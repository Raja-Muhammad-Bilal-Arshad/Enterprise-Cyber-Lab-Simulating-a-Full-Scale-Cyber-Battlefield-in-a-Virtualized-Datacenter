#!/usr/bin/env python3
"""
admin_tool.py
Safe, lab-only encrypted admin/diagnostic tool (server <-> agent)
- TLS encrypted channel
- Whitelisted commands only (no arbitrary shell)
- Polished CLI with rich
- Logging to timestamped files

USAGE (lab only):
  # server (operator)
  python3 admin_tool.py --mode server --host 0.0.0.0 --port 4433 --cert server.crt --key server.key

  # agent (run on test host)
  python3 admin_tool.py --mode agent --server-ip 192.168.100.50 --server-port 4433 \
      --cert agent.crt --key agent.key --ca server.crt

NOTE: Use only in controlled lab with permission.
"""
import argparse
import socket
import ssl
import threading
import time
import subprocess
import csv
from datetime import datetime
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# Safe whitelist of commands the agent can run
WHITELIST = {
    "hostname": ["hostname"],
    "whoami": ["whoami"],
    "uptime": ["uptime"],
    # safe 'ls' limited to allowed dir; agent will reject paths that traverse up
    "ls": ["ls"],
    "date": ["date"],
}

LOG_PREFIX = "admin_tool_log"

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def write_log(filename, data_rows):
    with open(filename, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for row in data_rows:
            w.writerow(row)

# ---------- Agent (client) ----------
def run_whitelisted(cmd_name, args):
    """Run only whitelisted commands. Args is a string (rest of input)."""
    if cmd_name not in WHITELIST:
        return False, f"Command not allowed: {cmd_name}"
    try:
        if cmd_name == "ls":
            # very limited ls: only allow relative single directory names, no .. segments
            safe_arg = args.strip() or "."
            if ".." in safe_arg or safe_arg.startswith("/"):
                return False, "Unsafe path; rejected."
            proc = subprocess.check_output(["ls", "-la", safe_arg], stderr=subprocess.STDOUT, timeout=10)
            return True, proc.decode(errors="ignore")
        else:
            proc = subprocess.check_output(WHITELIST[cmd_name], stderr=subprocess.STDOUT, timeout=10)
            return True, proc.decode(errors="ignore")
    except subprocess.CalledProcessError as e:
        return False, e.output.decode(errors="ignore")
    except Exception as e:
        return False, str(e)

def agent_mode(args):
    banner = Panel.fit("[bold green]AGENT MODE[/bold green]\nConnecting to server...", title="admin_tool", subtitle="agent")
    console.print(banner)
    server_addr = (args.server_ip, args.server_port)
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=args.ca)
    if args.cert and args.key:
        ctx.load_cert_chain(certfile=args.cert, keyfile=args.key)
    ctx.check_hostname = False

    log_file = f"{LOG_PREFIX}_agent_{timestamp()}.csv"
    try:
        raw = socket.create_connection(server_addr, timeout=10)
        ssock = ctx.wrap_socket(raw, server_side=False)
        console.print(f"[bold blue]Connected to[/bold blue] {server_addr}")
    except Exception as e:
        console.print(f"[red]Connection failed:[/red] {e}")
        return

    try:
        # simple handshake
        ssock.sendall(b"AGENT_HELLO\n")
        while True:
            data = ssock.recv(4096)
            if not data:
                break
            text = data.decode(errors="ignore").strip()
            # Expect commands like: RUN <cmdname> <args...>
            if text.startswith("RUN "):
                parts = text.split(" ", 2)
                if len(parts) >= 2:
                    cmd_name = parts[1]
                    cmd_args = parts[2] if len(parts) == 3 else ""
                    ok, output = run_whitelisted(cmd_name, cmd_args)
                    timestamp_now = datetime.now().isoformat()
                    ssock.sendall(f"RESPONSE {cmd_name} {str(ok)}\n{output}\n<<END>>\n".encode())
                    write_log(log_file, [[timestamp_now, cmd_name, ok, output.replace("\n", "\\n")]])
            elif text == "PING":
                ssock.sendall(b"PONG\n")
            elif text == "EXIT":
                break
            else:
                # unknown message -> ignore or log
                write_log(log_file, [[datetime.now().isoformat(), "UNKNOWN", text]])
    finally:
        try:
            ssock.shutdown(socket.SHUT_RDWR)
            ssock.close()
        except:
            pass
        console.print("[green]Agent disconnected.[/green]")

# ---------- Server (operator) ----------
def handle_client(connstream, addr, operator_state):
    console.print(f"[bold yellow]New secure connection from[/bold yellow] {addr}")
    try:
        # receive handshake
        initial = connstream.recv(1024).decode(errors="ignore").strip()
        if initial != "AGENT_HELLO":
            connstream.sendall(b"ERROR: Handshake failed\n")
            connstream.close()
            return
        # interactive loop
        while True:
            # operator_state supplies commands to send via a queue
            cmd = operator_state.get_next_command_for(addr)
            if cmd is None:
                # no commands; sleep a little
                time.sleep(0.2)
                continue
            if cmd == "EXIT":
                connstream.sendall(b"EXIT\n")
                break
            # send the command
            connstream.sendall(f"{cmd}\n".encode())
            # read responses until <<END>>
            resp = []
            while True:
                chunk = connstream.recv(4096)
                if not chunk:
                    break
                s = chunk.decode(errors="ignore")
                if "<<END>>" in s:
                    resp.append(s.split("<<END>>")[0])
                    break
                resp.append(s)
            # log
            operator_state.log_response(addr, cmd, "".join(resp))
    except Exception as e:
        console.print(f"[red]Client handler error:[/red] {e}")
    finally:
        try:
            connstream.close()
        except:
            pass
        console.print(f"[bold magenta]Connection from {addr} closed.[/bold magenta]")

class OperatorState:
    def __init__(self):
        self.lock = threading.Lock()
        self.command_queues = {}  # addr -> list of commands
        self.logs = []  # in-memory logs (also saved)

    def register_client(self, addr):
        with self.lock:
            self.command_queues.setdefault(addr, [])

    def enqueue_command(self, addr, cmd):
        with self.lock:
            if addr not in self.command_queues:
                self.command_queues[addr] = []
            self.command_queues[addr].append(cmd)

    def get_next_command_for(self, addr):
        with self.lock:
            q = self.command_queues.get(addr, [])
            if q:
                return q.pop(0)
            return None

    def log_response(self, addr, sent_cmd, response_text):
        row = [datetime.now().isoformat(), str(addr), sent_cmd, response_text.replace("\n", "\\n")]
        self.logs.append(row)
        write_log(f"{LOG_PREFIX}_server_{timestamp()}.csv", [row])

def server_mode(args):
    banner = Panel.fit("[bold red]SERVER (Operator) MODE[/bold red]\nWaiting for agent connections...", title="admin_tool", subtitle="server")
    console.print(banner)
    operator_state = OperatorState()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=args.cert, keyfile=args.key)
    if args.ca:
        context.load_verify_locations(cafile=args.ca)
        context.verify_mode = ssl.CERT_OPTIONAL

    bindsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsock.bind((args.host, args.port))
    bindsock.listen(5)

    console.print(f"[green]Listening on[/green] {args.host}:{args.port} (TLS)")

    # accept thread
    def accept_loop():
        while True:
            newsock, addr = bindsock.accept()
            try:
                connstream = context.wrap_socket(newsock, server_side=True)
            except ssl.SSLError as e:
                console.print(f"[red]SSL error on wrap_socket:[/red] {e}")
                newsock.close()
                continue
            operator_state.register_client(addr)
            t = threading.Thread(target=handle_client, args=(connstream, addr, operator_state), daemon=True)
            t.start()

    tacc = threading.Thread(target=accept_loop, daemon=True)
    tacc.start()

    # Operator interactive console
    console.print("[bold cyan]Operator console ready.[/bold cyan]")
    while True:
        console.print()
        console.print("[bold]Commands:[/bold] [green]list[/green], [green]send[/green], [green]log[/green], [green]exit[/green]")
        cmd = Prompt.ask("Enter command").strip()
        if cmd == "list":
            with operator_state.lock:
                if not operator_state.command_queues:
                    console.print("[yellow]No connected agents yet.[/yellow]")
                else:
                    console.print("Connected agents:")
                    for a in operator_state.command_queues.keys():
                        console.print(f" - {a}")
        elif cmd.startswith("send"):
            # send <ip:port> <RUN cmdname [args...]>
            try:
                _, target, *rest = cmd.split(" ")
                # try to parse target into tuple style
                # simple matching by string
                matched = None
                with operator_state.lock:
                    for a in operator_state.command_queues.keys():
                        if str(a[0]) == target or f"{a[0]}:{a[1]}" == target:
                            matched = a
                            break
                if not matched:
                    console.print(f"[red]Agent {target} not found.[/red]")
                    continue
                payload = " ".join(rest)
                # Validate payload starts with RUN
                if not payload.startswith("RUN "):
                    console.print("[red]Payload must start with 'RUN '. Example: RUN hostname[/red]")
                    continue
                operator_state.enqueue_command(matched, payload)
                console.print(f"[green]Queued to {matched}:[/green] {payload}")
            except Exception as e:
                console.print(f"[red]Error parsing send:[/red] {e}")
        elif cmd == "log":
            # print recent logs (from disk)
            console.print("[blue]Recent logs are written to CSV files (prefix: admin_tool_log_*)[/blue]")
        elif cmd == "exit":
            console.print("[yellow]Shutting down server...[/yellow]")
            break
        else:
            console.print("[red]Unknown command[/red]")

    bindsock.close()

# ---------- CLI and argparsing ----------
def main():
    parser = argparse.ArgumentParser(description="Safe lab admin tool (TLS + whitelist).")
    parser.add_argument("--mode", required=True, choices=["server", "agent"], help="Mode to run.")
    # server args
    parser.add_argument("--host", default="0.0.0.0", help="Server bind host (server mode).")
    parser.add_argument("--port", default=4433, type=int, help="Server port (server mode).")
    parser.add_argument("--cert", help="Path to cert file (server or agent).")
    parser.add_argument("--key", help="Path to key file (server or agent).")
    parser.add_argument("--ca", help="CA cert file (for mutual TLS or server validation).")

    # agent args
    parser.add_argument("--server-ip", help="Server IP to connect to (agent mode).")
    parser.add_argument("--server-port", type=int, default=4433, help="Server port (agent mode).")

    args = parser.parse_args()

    # Pretty banner
    banner = """
 █████╗ ██████╗ ███╗   ██╗███╗   ██╗██╗███████╗
██╔══██╗██╔══██╗████╗  ██║████╗  ██║██║██╔════╝
███████║██████╔╝██╔██╗ ██║██╔██╗ ██║██║█████╗
██╔══██║██╔═══╝ ██║╚██╗██║██║╚██╗██║██║██╔══╝
██║  ██║██║     ██║ ╚████║██║ ╚████║██║███████╗
╚═╝  ╚═╝╚═╝     ╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚══════╝
"""
    console.print(Panel(banner, title="admin_tool", subtitle=f"mode={args.mode}"))
    if args.mode == "server":
        if not args.cert or not args.key:
            console.print("[red]server mode requires --cert and --key[/red]")
            return
        server_mode(args)
    else:
        # agent
        if not args.server_ip:
            console.print("[red]agent mode requires --server-ip[/red]")
            return
        # copy server args into agent args for convenience
        args.server_port = args.server_port
        agent_mode(args)

if __name__ == "__main__":
    main()
