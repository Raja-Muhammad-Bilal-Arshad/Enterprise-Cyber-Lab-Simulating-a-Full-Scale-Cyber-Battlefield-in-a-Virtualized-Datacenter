#!/usr/bin/env python3
import threading
import time
from scapy.all import IP, TCP, UDP, ICMP, send

# ================================
# PFsense Rule Penetration Tester
# ================================
BANNER = """
==========================================
   PFsense Rule Penetration Tester v3.0
   Author: Friendly Red teamer
   Purpose: Simulate TCP/UDP/ICMP tests
==========================================
"""

def tcp_test(dst_ip, port):
    pkt = IP(dst=dst_ip) / TCP(dport=port, flags="S")
    send(pkt, verbose=False)

def udp_test(dst_ip, port):
    pkt = IP(dst=dst_ip) / UDP(dport=port) / b"TestPacket"
    send(pkt, verbose=False)

def icmp_test(dst_ip):
    pkt = IP(dst=dst_ip) / ICMP()
    send(pkt, verbose=False)

def worker(dst_ip, test_type, port, count):
    for _ in range(count):
        if test_type == "tcp":
            tcp_test(dst_ip, port)
        elif test_type == "udp":
            udp_test(dst_ip, port)
        elif test_type == "icmp":
            icmp_test(dst_ip)

def main():
    print(BANNER)

    # ====== Professional Menu ======
    print("[1] TCP Packet Test")
    print("[2] UDP Packet Test")
    print("[3] ICMP Flood Test")
    print("[0] Exit")
    print("==========================================")

    choice = input("[?] Select test type: ").strip()

    if choice == "0":
        print("[!] Exiting...")
        return

    dst_ip = input("[?] Enter Target IP Address: ").strip()

    if choice in ["1", "2"]:
        port = int(input("[?] Enter Target Port: ").strip())
    else:
        port = None

    threads = int(input("[?] Enter Number of Threads: ").strip())
    count = int(input("[?] Packets per Thread: ").strip())

    # Map menu choice to test type
    if choice == "1":
        test_type = "tcp"
    elif choice == "2":
        test_type = "udp"
    elif choice == "3":
        test_type = "icmp"
    else:
        print("[-] Invalid choice!")
        return

    # ====== Run the test ======
    start_time = time.time()
    thread_list = []

    for _ in range(threads):
        t = threading.Thread(target=worker, args=(dst_ip, test_type, port, count))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    duration = time.time() - start_time
    total_packets = threads * count
    print("\n==========================================")
    print(f"[+] Test Completed in {duration:.2f} seconds")
    print(f"[+] Total Packets Sent: {total_packets}")
    print("==========================================")

if __name__ == "__main__":
    main()
