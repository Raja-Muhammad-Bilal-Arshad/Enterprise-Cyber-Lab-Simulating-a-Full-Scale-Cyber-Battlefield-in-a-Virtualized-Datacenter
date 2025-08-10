# **Enterprise Cyber Lab:**

# Simulating a Full-Scale Cyber Battlefield in a Virtualized Datacenter

---

##  **Project Overview**

This project recreates an **entire enterprise network** inside a **Proxmox Virtual Environment**, then hardens it using **pfSense firewalls**, **Suricata IDS**, and **Snort IPS**, with **full log forwarding** into **Splunk SIEM** for real-time threat visibility.

Inside this **safe, isolated lab**, we stage a **live cyber battle**:

* **Attackers**: Distributed penetration testing nodes executing coordinated, multi-vector assaults.

* **Victims**: Windows & Linux systems running vulnerable services.

* **Defenders**: Firewalls, IDS/IPS, and SIEM analysts responding in real-time.

---

##  **Lab Objectives**

* Build a **realistic enterprise network** on virtualized infrastructure.

* Deploy **layered security** using pfSense, Suricata, Snort, and Pi-hole.

* Simulate **real-world cyber attacks** from multiple sources.

* Enable **blue team monitoring** through Splunk SIEM dashboards.

* Provide a **repeatable platform** for testing, training, and research.

---

##  **The Simulation Flow**

1. **Infrastructure Deployment**

   * Proxmox cluster hosts all attack, victim, and security nodes.

   * Segmented networks with pfSense as the gateway.

2. **Security Hardening**

   * Suricata & Snort for deep packet inspection.

   * Pi-hole for DNS filtering & ad/tracker blocking.

   * pfBlockerNG for geographic IP blocking.

3. **Attack Execution**

   * Kali Linux “Major” node commands botnet-style “Soldier” nodes.

   * Custom socket-based flooders, scanners, and exploit scripts.

4. **Defensive Response**

   * IDS signatures trigger alerts.

   * Firewalls block suspicious IPs in real-time.

   * Splunk dashboards light up with events.

5. **Incident Analysis**

   * Timeline reconstruction of the “battle.”

   * Review of firewall logs, IDS hits, and SIEM correlation.

---

##  **Module Index**

Click any module to explore details.
## 📜 Index
- [Module 1 – Proxmox Virtualized Datacenter Cluster](Module%201:%20Proxmox%20Virtualized%20Datacenter%20Cluster)
- [Module 2 – pfSense Firewall & Gateway Architecture](Module%202%20–%20pfSense%20Firewall%20%26%20Gateway%20Architecture)
- [Module 3 – Inline Network Security with Suricata, Snort & pfBlockerNG in pfSense](Module%203:%20Inline%20Network%20Security%20with%20Suricata,%20Snort%20%26%20pfBlockerNG%20in%20pfSense)
- [Module 4 – Centralized Logging & SIEM with Splunk](Module%204:%20Centralized%20Logging%20%26%20SIEM%20with%20Splunk)
- [Module 5 – Ad & Tracker Blocking with Pi-hole DNS Sinkhole](Module%205:%20Ad%20%26%20Tracker%20Blocking%20with%20Pi-hole%20DNS%20Sinkhole)
- [Module 6 – Few Penetration Testing Scripts](Module%206:%20Few%20Penetration%20Testing%20Scripts)
- [Module 7 – Centralized SIEM with Splunk](Module%207:Centralized%20SIEM%20with%20SPLUNK)
- [Module 8 – Distributed Penetration Testing & Defence Evaluation](Module%208:Distirbuted%20Penetration%20Testing%20%26%20Defence%20Evaluation)
- [Module 9 – Secure Remote Access With ZeroTier](Module%209:%20Secure%20Remote%20Access%20With%20ZeroTier)

##  **Technology Stack**

* **Virtualization:** Proxmox VE

* **Firewall:** pfSense

* **IDS/IPS:** Suricata, Snort

* **SIEM:** Splunk Enterprise

* **DNS Filtering:** Pi-hole

* **Attack Toolkit:** Kali Linux, Python, Bash

* **Remote Access:** ZeroTier

---

## **Professional Disclaimer**

## This project and all associated materials are created and maintained by a **professional penetration tester** in offensive and defensive cybersecurity operations.

## All demonstrations, simulations, scripts, configurations, and attack scenarios contained within this repository are intended **solely for use in authorized, controlled, and isolated environments** such as lab networks, virtualized testbeds, and academic/research setups.

## **No part of this work is to be executed, replicated, or adapted against any live, production, or internet-facing system without prior *written* consent from the legitimate system owner.**

## The author **does not assume any liability** for misuse, damages, or legal consequences resulting from the use or deployment of the materials herein outside of their intended purpose.  By accessing or using any part of this repository, you acknowledge and agree that:

1. ## You are solely responsible for your actions. 

2. ## You will comply with all applicable local, national, and international laws. 

3. ## You will obtain proper authorization before engaging in any penetration testing or security research outside of a lab environment. 

## This repository is published for:

* ## Professional training 

* ## Academic research 

* ## Security awareness 

* ## Authorized penetration testing methodology demonstration 

##  **If you are not fully aware of the legal boundaries of penetration testing, stop immediately and seek professional guidance.** Unauthorized use of these techniques can result in severe criminal and civil penalties.

## 

