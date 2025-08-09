#!/usr/bin/env python3
import argparse
import os
import sys
import time
from scapy.all import *

# ---------------- Banner ----------------
def banner():
    os.system("clear")
    print("\033[1;31m" + r"""
   ███████╗██╗██████╗ ██╗    ██╗██╗██╗     ██╗
   ██╔════╝██║██╔══██╗██║    ██║██║██║     ██║
   █████╗  ██║██████╔╝██║ █╗ ██║██║██║     ██║
   ██╔══╝  ██║██╔═══╝ ██║███╗██║██║██║     ██║
   ██║     ██║██║     ╚███╔███╔╝██║███████╗██║
   ╚═╝     ╚═╝╚═╝      ╚══╝╚══╝ ╚═╝╚══════╝╚═╝
        pfSense Rule Penetration Tester
        By: Your Friendly Red Teamer
    """ + "\033[0m")
    print("\033[1;37m" + "="*60)
    print("   ⚡ Simulate TCP/UDP/ICMP traffic to test firewall rules")
    print("   ⚡ Perform controlled scans & rule-bypass simulations")
    print("="*60 + "\033[0m\n")

# ---------------- Menu ----------------
def menu():
    print("\033[1;36m[1] TCP Port Scan")
    print("[2] UDP Port Scan")
    print("[3] ICMP Ping Flood")
    print("[4] VPN Bypass Simulation")
    print("[5] Exit\033[0m\n")

# ---------------- Attack Simulations ----------------
def tcp_port_scan(target):
    print(f"[+] Starting TCP port scan on {target}...")
    for port in range(20, 1025):
        pkt = IP(dst=target)/TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=0.5, verbose=0)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
            print(f"   [OPEN] TCP {port}")
            sr(IP(dst=target)/TCP(dport=port, flags="R"), timeout=0.5, verbose=0)
    print("[+] TCP scan complete.\n")

def udp_port_scan(target):
    print(f"[+] Starting UDP port scan on {target}...")
    for port in range(20, 1025):
        pkt = IP(dst=target)/UDP(dport=port)
        resp = sr1(pkt, timeout=0.5, verbose=0)
        if not resp:
            print(f"   [OPEN|FILTERED] UDP {port}")
    print("[+] UDP scan complete.\n")

def icmp_flood(target):
    print(f"[+] Launching ICMP flood to {target} (CTRL+C to stop)...")
    pkt = IP(dst=target)/ICMP()
    try:
        send(pkt, loop=1, inter=0.05, verbose=0)
    except KeyboardInterrupt:
        print("\n[+] Stopped ICMP flood.\n")

def vpn_bypass_attempt(target):
    print(f"[+] Simulating VPN bypass attempts on {target}...")
    fake_ips = ["10.8.0.2", "172.16.5.4", "100.64.12.7"]
    for fake_ip in fake_ips:
        pkt = IP(src=fake_ip, dst=target)/TCP(dport=443, flags="S")
        send(pkt, verbose=0)
        print(f"   [SENT] Spoofed packet from {fake_ip}")
    print("[+] VPN bypass simulation complete.\n")

# ---------------- Main ----------------
if __name__ == "__main__":
    banner()
    target = input("\033[1;33mEnter target IP: \033[0m")
    
    while True:
        menu()
        choice = input("\033[1;37mSelect an option: \033[0m")
        
        if choice == "1":
            tcp_port_scan(target)
        elif choice == "2":
            udp_port_scan(target)
        elif choice == "3":
            icmp_flood(target)
        elif choice == "4":
            vpn_bypass_attempt(target)
        elif choice == "5":
            print("[+] Exiting. Stay stealthy, hacker.")
            sys.exit()
        else:
            print("[-] Invalid choice. Try again.")
