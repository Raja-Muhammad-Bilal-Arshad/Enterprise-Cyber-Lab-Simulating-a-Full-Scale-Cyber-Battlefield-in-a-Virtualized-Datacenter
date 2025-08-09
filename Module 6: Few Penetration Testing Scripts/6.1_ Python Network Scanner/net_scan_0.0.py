import socket
import threading
import ipaddress
from queue import Queue
import time
import os
import platform
import csv
from datetime import datetime

# ========== GLOBALS ==========
scan_queue = Queue()
print_lock = threading.Lock()
results = []

# ======= COMMON UDP PORTS (Top 10) ==========
COMMON_UDP_PORTS = [53, 67, 68, 69, 123, 161, 162, 500, 514, 520]

# ========== INPUT MENU ==========
def get_user_input():
    print("\n💻 === Network Scanner Config Menu ===")
    subnet = input("🌐 Enter target subnet (default 192.168.1.0/24): ") or "192.168.1.0/24"
    port_range_input = input("🔢 Enter TCP port range (e.g., 1-65535 or 20-1000): ") or "1-1024"
    port_start, port_end = map(int, port_range_input.split('-'))
    timeout = float(input("⏱️ Enter socket timeout in seconds (default 0.5): ") or 0.5)
    threads = int(input("🧵 Enter max threads (default 300, max 1000): ") or 300)
    threads = min(threads, 1000)
    return subnet, port_start, port_end, timeout, threads

# ========== PING CHECK (LIVE HOSTS) ==========
def is_host_alive(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '1', ip]
    return os.system(" ".join(command)) == 0

# ========== TCP SCANNER ==========
def tcp_scan(ip, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                banner = s.recv(1024).decode(errors='ignore').strip()
            except:
                banner = "No banner"
            with print_lock:
                print(f"[🔓 TCP] {ip}:{port} OPEN → {banner}")
            results.append((ip, port, 'TCP', 'OPEN', banner))
        s.close()
    except:
        pass

# ========== UDP SCANNER ==========
def udp_scan(ip, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        s.sendto(b"", (ip, port))
        data, _ = s.recvfrom(1024)
        with print_lock:
            print(f"[🟡 UDP] {ip}:{port} → Response received")
        results.append((ip, port, 'UDP', 'OPEN/RESPONDED', data.decode(errors='ignore').strip()))
    except socket.timeout:
        results.append((ip, port, 'UDP', 'NO RESPONSE', 'Likely open or filtered'))
    except:
        results.append((ip, port, 'UDP', 'ERROR', 'No response'))
    finally:
        s.close()

# ========== WORKER THREAD ==========
def worker(timeout):
    while not scan_queue.empty():
        ip, port, protocol = scan_queue.get()
        if protocol == "TCP":
            tcp_scan(ip, port, timeout)
        elif protocol == "UDP":
            udp_scan(ip, port, timeout)
        scan_queue.task_done()

# ========== CSV SAVER ==========
def save_results_to_csv():
    filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['IP', 'Port', 'Protocol', 'Status', 'Banner/Response'])
        writer.writerows(results)
    print(f"\n📁 Results saved to: {filename}")

# ========== MAIN ==========
def main():
    subnet, port_start, port_end, timeout, max_threads = get_user_input()
    start = time.time()
    live_hosts = []

    print("\n🔍 Detecting live hosts...\n")
    for ip in ipaddress.IPv4Network(subnet, strict=False).hosts():
        ip_str = str(ip)
        if is_host_alive(ip_str):
            print(f"[✅] Host is UP: {ip_str}")
            live_hosts.append(ip_str)

    if not live_hosts:
        print("❌ No live hosts found.")
        return

    print(f"\n🔎 Scanning {len(live_hosts)} live hosts for TCP + UDP...\n")

    for ip in live_hosts:
        for port in range(port_start, port_end + 1):
            scan_queue.put((ip, port, "TCP"))
        for port in COMMON_UDP_PORTS:
            scan_queue.put((ip, port, "UDP"))

    thread_count = min(max_threads, scan_queue.qsize())
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(timeout,), daemon=True)
        t.start()

    scan_queue.join()
    end = time.time()
    print(f"\n✅ Scan completed in {round(end - start, 2)} seconds.")
    save_results_to_csv()

if __name__ == '__main__':
    main()
