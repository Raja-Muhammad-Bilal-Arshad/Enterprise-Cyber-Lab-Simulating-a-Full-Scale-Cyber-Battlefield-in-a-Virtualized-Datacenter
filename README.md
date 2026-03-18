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

![Cyber lab image](Assets/Module%201/1.1.png)

##  **Lab Objectives**

* Build a **realistic enterprise network** on virtualized infrastructure.

* Deploy **layered security** using pfSense, Suricata, Snort, and Pi-hole.

* Simulate **real-world cyber attacks** from multiple sources.

* Enable **blue team monitoring** through Splunk SIEM dashboards.

* Provide a **repeatable platform** for testing, training, and research.

---
![Cyber lab image](/Assets/Module%204/4.9.png)

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
![Cyber lab image](Assets/Module%207/7.3.png)

##  **Module Index**

Click any module to explore details.
## 📜 Index

- [Module 1 – Proxmox Virtualized Datacenter Cluster](Module%201%3A%20Proxmox%20Virtualized%20Datacenter%20Cluster/Module%201%20%E2%80%93%20Proxmox%20Virtualized%20Datacenter%20Cluster.md)
- [Module 2 – pfSense Firewall & Gateway Architecture](Module%202%20%E2%80%93%20pfSense%20Firewall%20%26%20Gateway%20Architecture/Module%202%20%E2%80%93%20pfSense%20Firewall%20%26%20Gateway%20Architecture.md)
- [Module 3 – Inline Network Security with Suricata, Snort & pfBlockerNG in pfSense](Module%203%3A%20Inline%20Network%20Security%20with%20Suricata%2C%20Snort%20%26%20pfBlockerNG%20in%20pfSense/Module%203_%20Inline%20Network%20Security%20with%20Suricata%2C%20Snort%20%26%20pfBlockerNG%20in%20pfSense.md)
- [Module 4 – Centralized Logging & SIEM with Splunk](Module%204%3A%20Centralized%20Logging%20%26%20SIEM%20with%20Splunk/Module%204_%20Centralized%20Logging%20%26%20SIEM%20with%20Splunk.md)
- [Module 5 – Ad & Tracker Blocking with Pi-hole DNS Sinkhole](Module%205%3A%20Ad%20%20%26%20Tracker%20Blocking%20with%20Pi-hole%20DNS%20Sinkhole/Module%205_%20Ad%20%26%20Tracker%20Blocking%20with%20Pi-hole%20DNS%20Sinkhole.md)
- [Module 6 – Few Penetration Testing Scripts](Module%206%3A%20Few%20Penetration%20Testing%20Scripts/6.1_%20Python%20Network%20Scanner/6.1_%20Python%20Network%20Scanner.md)
- [Module 7 – Centralized SIEM with Splunk](Module%207%3ACentralized%20SIEM%20with%20SPLUNK/Module%207_%20Centralized%20SIEM%20with%20Splunk.md)
- [Module 8 – Distributed Penetration Testing & Defence Evaluation](Module%208%3ADistirbuted%20Penetration%20Testing%20%20%26%20%20Defence%20Evaluation/Module%208_%20Distributed%20Penetration%20Testing%20%26%20Defense%20Evaluation.md)
- [Module 9 – Secure Remote Access With ZeroTier](Module%209%3A%20Secure%20Remote%20Access%20With%20ZeroTier/Module%209%20%E2%80%93%20Secure%20Remote%20Access%20with%20ZeroTier.md)

![Cyber lab image](Assets/Module%208/8.5.png)

##  **Technology Stack**

* **Virtualization:** Proxmox VE

* **Firewall:** pfSense

* **IDS/IPS:** Suricata, Snort

* **SIEM:** Splunk Enterprise

* **DNS Filtering:** Pi-hole

* **Attack Toolkit:** Kali Linux, Python, Bash

* **Remote Access:** ZeroTier

---
## Use Cases

This project is designed for a wide range of cybersecurity applications:

- 🔴 Red Team / Blue Team simulation environments  
- 🏫 Academic cybersecurity labs and university research  
- 🛡️ Security operations (SOC) training platforms  
- 🔍 SIEM testing and log analysis practice  
- 🧪 Malware analysis and controlled attack simulations  
- 👨‍💻 Hands-on learning for penetration testers and security engineers
- 
## Who Should Use This Project

- Cybersecurity students and researchers  
- Penetration testers and ethical hackers  
- Security engineers and SOC analysts  
- Educators building hands-on lab environments  
- Developers interested in secure infrastructure and attack simulation 

## ⚙️ Quick Deployment Overview

1. Set up a Proxmox Virtual Environment  
2. Deploy pfSense as the network gateway  
3. Configure segmented internal networks  
4. Install IDS/IPS tools (Suricata, Snort)  
5. Integrate Splunk SIEM for centralized logging  
6. Deploy attacker and victim machines  
7. Execute controlled attack simulations and monitor responses  

> Full step-by-step instructions are available in the module documentation.

## 🤝 Contributing

Contributions are welcome to improve this cybersecurity lab and expand its capabilities.

You can contribute by:

- Adding new attack or defense modules  
- Improving documentation and lab guides  
- Enhancing automation scripts  
- Reporting issues or suggesting improvements  

Please ensure all contributions follow ethical security practices.

## 🧠 Future Roadmap

- Automated attack scenario generation  
- AI-assisted log analysis and threat detection  
- Integration with additional SIEM platforms  
- Expanded red team / blue team scenarios  
- Cloud-based lab deployment options

## 🌍 Community & Impact

This project aims to provide an open, accessible platform for cybersecurity education and research.

By simulating real-world enterprise environments, it helps bridge the gap between theoretical knowledge and practical skills, enabling learners and professionals to safely experiment, analyze, and improve their security capabilities.

The long-term goal is to build a comprehensive open-source ecosystem for cybersecurity training and simulation.

 # **Disclaimer**

 This project and all associated materials are created and maintained by a **professional penetration tester** in offensive and defensive cybersecurity operations.

 All demonstrations, simulations, scripts, configurations, and attack scenarios contained within this repository are intended **solely for use in authorized, controlled, and isolated environments** such as lab networks, virtualized testbeds, and academic/research setups.

 **No part of this work is to be executed, replicated, or adapted against any live, production, or internet-facing system without prior *written* consent from the legitimate system owner.**

 The author **does not assume any liability** for misuse, damages, or legal consequences resulting from the use or deployment of the materials herein outside of their intended purpose.  By accessing or using any part of this repository, you acknowledge and agree that:

1.  You are solely responsible for your actions. 

2.  You will comply with all applicable local, national, and international laws. 

3.  You will obtain proper authorization before engaging in any penetration testing or security research outside of a lab environment. 

 This repository is published for:

*  Professional training 

*  Academic research 

*  Security awareness 

*  Authorized penetration testing methodology demonstration 

  **If you are not fully aware of the legal boundaries of penetration testing, stop immediately and seek professional guidance.** Unauthorized use of these techniques can result in severe criminal and civil penalties.



