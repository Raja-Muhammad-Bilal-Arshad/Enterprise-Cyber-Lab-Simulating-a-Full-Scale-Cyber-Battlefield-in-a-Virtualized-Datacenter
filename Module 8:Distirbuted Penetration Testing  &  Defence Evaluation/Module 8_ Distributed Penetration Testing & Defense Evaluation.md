## **Module 8:  Distributed Penetration Testing & Defense Evaluation**

### **Overview**

Module 8 replicates a **Distributed Penetration Testing & Defense Evaluation traffic environment** to enable **advanced penetration testing** and **defense validation** in a controlled, virtualized datacenter setup.  
 The architecture consists of **dedicated attack nodes**, **diverse target systems**, and **layered perimeter security** — all monitored via **Splunk SIEM** for real-time detection and analysis.

This simulation is designed to:

* Validate **firewall rules**, **IDS/IPS signatures**, and **endpoint protections** under realistic attack conditions.

* Provide a **repeatable testbed** for network defense experiments.

* Showcase **distributed attack coordination** from multiple nodes.

---

### **Infrastructure Layout**

**Attack Infrastructure:**

* **Major (Kali Linux):** Centralized offensive command and control node.

* **Soldier1–4 (Ubuntu Servers):** Distributed attack executors simulating botnet-style activity.

**Target Infrastructure:**

* **TestSubject001–006 (Windows \+ Linux):** Mimic real-world endpoints with varied services and vulnerabilities.

**Network Protection:**

* **pfSense Firewalls:** Enforce strict perimeter and inter-segment security.

* **Suricata IDS(And SNORT):** Provides real-time intrusion detection with custom rules.

* **Splunk SIEM:** Central log aggregation, correlation, and alerting.

| Feature | Description |
| :---- | ----- |
| **Distributed Attacks** | Multi-node, coordinated scans, floods, and intrusion attempts. |
| **DNS Spoofing & Redirection** | Manipulate DNS responses to test client resilience. |
| **Host & Network Defense** | Validate firewall rules, endpoint IDS, and anti-malware reactions. |
| **Traffic Analytics** | Monitor real-time flow data and detect anomalies. |
| **Incident Response** | Generate alerts and timelines for attack events in SIEM. |

![Cyber lab image](../Assets/Module%208/8.1.png)

### **Real-World Scenario Simulation**

1. **Botnet Emulation:** Soldiers launch simultaneous, varied attacks.

2. **Cross-Platform Testing:** Targets include both Windows and Linux systems.

3. **Dynamic Defenses:** Endpoints actively detect and mitigate incoming threats.

4. **Centralized Monitoring:** SIEM captures complete activity logs for post-attack analysis.

### **Example Use Cases**

* **Multi-Vector DDoS Simulation:** Soldiers flood a target while Major executes crafted packet probes.

* **DNS Security Validation:** Redirect domain queries and measure defense reaction.

* **Suricata Rule Testing:** Trigger alerts using specific exploit signatures.

* **Firewall Bypass Attempts:** Attempt VPN-based perimeter bypass under pfSense.

![Cyber lab image](../Assets/Module%208/8.2.png)

### **Deployment Steps**

1. **Launch All VMs** on the Proxmox cluster with required specifications.

2. **Configure pfSense:**

   * Set firewall rules for attack and target zones.

   * Enable IDS/IPS policies.

3. **Prepare Attack Nodes:**

   * Install required tools (Nmap, Hping3, Metasploit, etc.).

4. **Start Simulation:**

   * Coordinate attacks from Major and Soldiers.

   * Execute pre-designed penetration scenarios.

5. **Monitor via Splunk SIEM:**

   * Track live alerts, events, and traffic statistics.

6. **Analyze Results:**

   * Identify missed detections and tune defense mechanisms.

---

### **Performance & Outcomes**

* **Layered Security Validation:** Proves the resilience of firewall \+ IDS \+ endpoint protection.

* **High Fidelity Simulation:** Accurately mimics distributed cyberattack conditions.

* **SIEM Effectiveness:** Demonstrates real-time event correlation and actionable alerting.

* **Repeatable Testing Environment:** Enables continuous security improvement cycles.

---

### **Skills Demonstrated**

* Advanced **network simulation** in virtualized environments.

* Offensive and defensive **cybersecurity operations**.

* **SIEM integration** for incident detection and reporting.

* **Firewall & IDS policy tuning** in real-world-like conditions.

* Coordinated **multi-node attack execution**.

## **Proxmox Environment – Pentesting Lab**

### **1\. Proxmox Server (Database Node)**

* **CPU:** 8 Cores (15% average usage)

* **Memory:** 32 GB total (67% in use)

* **Storage:** 936.36 GB total (4% used)

* **IP Address:** 100.100.100.\*

* **Role:** Hypervisor hosting all pentesting virtual machines and networks

![Cyber lab image](../Assets/Module%208/8.3.png)
| VM ID | Name | Description | OS / Purpose | CPU Allocation | Memory Allocation | Status |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 100 | Major | Main attack machine | Kali Linux (Pentesting toolkit) | 4 cores | 3 GB | Running |
| 101 | Soldier1 | Attack client | Ubuntu Server(Red team) | 4 cores | 2 GB | Running |
| 102 | Soldier2 | Attack client | Ubuntu Server(Red team) | 4 cores | 2 GB | Running |
| 103 | Soldier3 | Attack client | Ubuntu Server(Red team) | 4 cores | 2 GB | Running |
| 104 | Soldier4 | Attack client | Ubuntu Server(Red team) | 4 cores | 2 GB | Running |
| 105 | Pfsense | Firewall & Routing | pfSense(Firewall) | 2 cores | 3 GB | Running |
| 106 | TestSubject001 | Target machine | Windows (victim) | 2 cores | 2 GB | Stopped |
| 107 | TestSubject002 | Target machine | Linux (victim) | 2 cores | 2 GB | Stopped |
| 108 | TestSubject003 | Target machine | Windows(victim) | 8 cores | 2 GB | Running |
| 109 | TestSubject004 | Target machine | Linux (victim) | 2 cores | 2 GB | Stopped |
| 110 | TestSubject005 | Target machine | Windows (victim) | 2 cores | 2 GB | Stopped |
| 111 | TestSubject006 | Target machine | Linux (victim) | 2 cores | 2 GB | Stopped |

### **3\. Network Setup**

* **Local Network:** `localNetwork (Database)`

* **Purpose:** Isolated pentesting lab for controlled simulations

* **Firewall:** pfSense for segmentation and filtering

* **VM Interconnectivity:** All VMs connected for attack-defense testing

![Cyber lab image](../Assets/Module%208/8.4.png)
### **4\. Pentesting Activities Performed**

You, as the **Professional Penetration Tester**, executed attacks for demonstration and educational purposes in a controlled lab.

#### **Attacks from Socket Programming Module**

* **Custom Port Scanner**

* **TCP SYN Flood**

* **UDP Flood**

* **ICMP Echo Storm**

* **Reverse Shells**

* **Simple RAT Simulation**

* **Brute-force Socket Authentication**
* 
![Cyber lab image](../Assets/Module%208/8.5.png)

#### **Additional Attacks**

* **Distributed Denial of Service (DDoS)** using Soldier1–4

* **Firewall Evasion** via crafted packets

* **Lateral Movement** across target VMs

* **Credential Harvesting** from compromised systems

* **Exploitation of Weak Services** (HTTP, SMB, FTP)

* **Packet Sniffing & MITM** attacks with `ettercap` and `bettercap`

![Cyber lab image](../Assets/Module%208/8.6.png)
![Cyber lab image](../Assets/Module%208/8.7.png)
![Cyber lab image](../Assets/Module%208/8.8.png)
