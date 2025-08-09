import socket
import ipaddress
import csv
import concurrent.futures
import subprocess
import datetime
from tqdm import tqdm

# ---------- Ping Function ----------
def ping_host(host):
    try:
        output = subprocess.run(
            ["ping", "-c", "1", "-W", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return output.returncode == 0
    except:
        return False

# ---------- Quick TCP Liveness Check ----------
def quick_tcp_check(host):
    common_ports = [22, 80, 443, 3389]
    for port in common_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((host, port)) == 0:
                    return True
        except:
            pass
    return False

# ---------- TCP Port Scan ----------
def scan_tcp_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                return port
    except:
        return None

# ---------- UDP Port Scan ----------
def scan_udp_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(b"", (host, port))
            try:
                data, _ = s.recvfrom(1024)
                return port
            except socket.timeout:
                return port  # UDP no response can still be "open|filtered"
    except:
        return None

# ---------- Main Script ----------
def main():
    print("\n--- Network Scanner ---\n")
    subnet_input = input("Enter subnet to scan (e.g. 192.168.1.0/24): ").strip()
    port_range_input = input("Enter TCP port range for detailed scan (e.g. 1-65535): ").strip()
    timeout = float(input("Enter max socket timeout (seconds): ").strip())
    max_threads = int(input("Enter max threads: ").strip())
    scan_udp_choice = input("Do you want to scan all UDP ports as well? (yes/no): ").strip().lower()

    start_port, end_port = map(int, port_range_input.split('-'))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_results_{timestamp}.csv"

    print("\n[*] Scanning for live hosts...\n")
    live_hosts = []
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(
            lambda ip: ip if ping_host(str(ip)) or quick_tcp_check(str(ip)) else None, ip
        ): ip for ip in ipaddress.IPv4Network(subnet_input, strict=False)}

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Host Discovery", unit="host"):
            result = future.result()
            if result:
                live_hosts.append(str(result))

    print(f"\n[+] Found {len(live_hosts)} live hosts.\n")

    results = []

    for host in live_hosts:
        print(f"[*] Scanning {host}...")
        tcp_open_ports = []
        udp_open_ports = []

        # TCP Scan
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            tcp_futures = {executor.submit(scan_tcp_port, host, port, timeout): port for port in range(start_port, end_port+1)}
            for future in tqdm(concurrent.futures.as_completed(tcp_futures), total=len(tcp_futures), desc=f"TCP Scan {host}", unit="port"):
                port = future.result()
                if port:
                    tcp_open_ports.append(port)

        # UDP Scan (if chosen)
        if scan_udp_choice == "yes":
            with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
                udp_futures = {executor.submit(scan_udp_port, host, port, timeout): port for port in range(1, 65536)}
                for future in tqdm(concurrent.futures.as_completed(udp_futures), total=len(udp_futures), desc=f"UDP Scan {host}", unit="port"):
                    port = future.result()
                    if port:
                        udp_open_ports.append(port)

        results.append({
            "Host": host,
            "TCP Open Ports": tcp_open_ports,
            "UDP Open Ports": udp_open_ports if scan_udp_choice == "yes" else []
        })

    # Save results to CSV
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Host", "TCP Open Ports", "UDP Open Ports"])
        writer.writeheader()
        for row in results:
            writer.writerow({
                "Host": row["Host"],
                "TCP Open Ports": ', '.join(map(str, row["TCP Open Ports"])),
                "UDP Open Ports": ', '.join(map(str, row["UDP Open Ports"]))
            })

    print(f"\n[+] Scan complete. Results saved to {filename}")

if __name__ == "__main__":
    main()
