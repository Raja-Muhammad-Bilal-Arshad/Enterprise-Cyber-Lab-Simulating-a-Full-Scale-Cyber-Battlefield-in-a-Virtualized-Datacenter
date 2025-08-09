import socket
import threading
import csv
from queue import Queue
from ipaddress import ip_network
import time
import os

# ========== CONFIG ==========
SUBNET = '192.168.1.0/24'
PORT_RANGE = (1, 1024)
UDP_PORTS = [53, 69, 123, 161, 500]
SOCKET_TIMEOUT = 0.5
MAX_THREADS = 500
OUTPUT_FILE = "scan_results.csv"
# ============================

vuln_ports = {
    23: "Telnet (Insecure)",
    21: "FTP (Unencrypted)",
    139: "NetBIOS (Legacy)",
    445: "SMB (WannaCry risk)",
    3389: "RDP (Targeted in brute-force attacks)",
    3306: "MySQL (Default creds?)",
    5900: "VNC (Often exposed)"
}

lock = threading.Lock()
live_hosts = []
queue = Queue()
results = []

def os_fingerprint(ttl):
    if ttl >= 128:
        return "Windows (guess)"
    elif 64 <= ttl < 128:
        return "Linux/Unix (guess)"
    else:
        return "Unknown"

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(SOCKET_TIMEOUT)
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
                except:
                    ttl = 64
                os_guess = os_fingerprint(ttl)
                vuln = vuln_ports.get(port, "")
                with lock:
                    results.append([ip, port, "TCP", os_guess, vuln])
    except:
        pass

def scan_udp_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(SOCKET_TIMEOUT)
            s.sendto(b'', (ip, port))
            s.recvfrom(1024)
            with lock:
                results.append([ip, port, "UDP", "N/A", ""])
    except socket.timeout:
        with lock:
            results.append([ip, port, "UDP", "N/A", ""])
    except:
        pass

def scan_worker():
    while not queue.empty():
        ip, port = queue.get()
        scan_port(ip, port)
        queue.task_done()

def udp_scan_worker(ip):
    for port in UDP_PORTS:
        scan_udp_port(ip, port)

def is_host_alive(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(SOCKET_TIMEOUT)
            if s.connect_ex((ip, 80)) == 0 or s.connect_ex((ip, 443)) == 0:
                return True
    except:
        return False
    return False

def write_results():
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Port", "Protocol", "OS Guess", "Vulnerability"])
        for row in results:
            writer.writerow(row)
    print(f"🔐 Results saved to {OUTPUT_FILE}")

def main():
    print(f"🔍 Scanning subnet {SUBNET} for live hosts...")
    hosts = [str(ip) for ip in ip_network(SUBNET).hosts()]
    for ip in hosts:
        if is_host_alive(ip):
            print(f"🟢 Host {ip} is alive")
            live_hosts.append(ip)

    if not live_hosts:
        print("⚠️ No live hosts found!")
        return

    print(f"\n⚡ Scanning ports {PORT_RANGE[0]} to {PORT_RANGE[1]} on {len(live_hosts)} live hosts...")

    for ip in live_hosts:
        for port in range(PORT_RANGE[0], PORT_RANGE[1] + 1):
            queue.put((ip, port))

    threads = []
    for _ in range(MAX_THREADS):
        t = threading.Thread(target=scan_worker)
        t.daemon = True
        threads.append(t)
        t.start()

    for ip in live_hosts:
        threading.Thread(target=udp_scan_worker, args=(ip,)).start()

    queue.join()
    time.sleep(1)  # Allow UDP threads to finish

    write_results()

if __name__ == "__main__":
    main()
