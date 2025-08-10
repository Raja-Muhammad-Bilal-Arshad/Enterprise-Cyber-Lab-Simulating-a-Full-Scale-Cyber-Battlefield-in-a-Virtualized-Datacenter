#  **Module 2 – pfSense Firewall & Gateway Architecture**

### ***Securing the Perimeter with Hierarchical Routing, Firewall Rules & VPN Access***

---

##  **Overview**

This module establishes a **centralized gateway and firewall layer** using **pfSense**, an open-source FreeBSD-based firewall and router. It acts as the heart of the network’s security perimeter and handles:

* Firewalling and NAT

* VLAN-aware routing

* DNS redirection to Pi-hole

* VPN remote access (OpenVPN with custom CA)

* Time-based and role-based firewall rules

---

##  **Hierarchical Routing Topology**

The network follows a **multi-hop gateway architecture** to simulate layered security zones:

```yaml  
Proxmox3 (WAN Simulation)  
      ↓  
Proxmox1 (Gateway & Security) — pfSense (Main Router/Firewall)  
      ↓  
Proxmox2 (SIEM Monitoring) — pfSense (Internal Security Firewall)  
```  
---

##  **Key Features Implemented**

*  pfSense as **primary gateway** on Proxmox1 VM

*  **Hierarchical routing** between nodes using pfSense firewalls

*  **Scheduled firewall rules** (restrict access by time or category)

*  **OpenVPN server** setup with custom certificate authority (CA)

*  **DNS redirection** to Pi-hole for ad and malicious domain blocking

*  **Role-based IP allocation** for Students, Staff, Admins

---

##  **VM Configuration for pfSense**

Create a pfSense VM on **Proxmox1** with:

* **RAM**: 2 GB

* **Storage**: 100 GB

* **NICs**:

  * vmbr0 – WAN (connected to Proxmox3’s pfSense)

  * vmbr1 – LAN (connected to internal network)

  * Optional: VLAN-aware interfaces

Attach an ISO of pfSense (e.g., pfSense-CE-2.7.2-RELEASE-amd64.iso) and install normally.

---

##  **Interface Configuration**

During pfSense install:

Assign interfaces:  
WAN  → vmbr0 (e.g., 192.168.100.1/24)  
LAN  → vmbr1 (e.g., 10.10.16.20/21)

* Enable DHCP on LAN

* Disable DHCP on WAN(I have enabled on LAN and disabled on WAN don't mind it….)  
![Cyber lab image](../Assets/Module%202/2.1.png)
---

##  **Firewall Rule Setup**

### **🔸 Basic Rules**

* **WAN interface**:

  * Allow OpenVPN (UDP 1194\)

  * Block all else (default)

* **LAN interface**:

  * Allow outbound internet

  * Redirect DNS to Pi-hole

### **🔸 Time-Based Rules**

* Go to: Firewall \> Schedules

* Create a schedule (e.g., NightBlock 10PM–6AM)

* Create rules and assign that schedule:

  * Block social media ports (TCP 443/80 with aliases like Facebook, YouTube)

  * Apply to Student VLAN or IP range

---

##  **VPN: OpenVPN Server Setup**

### **Step 1: Install OpenVPN Export Package**

Go to:

System \> Package Manager \> Available Packages \> openvpn-client-export  
![Cyber lab image](../Assets/Module%202/2.2.png)
Install it.

---

### **Step 2: Create a Certificate Authority (CA)**

System \> Cert. Manager \> CAs \> Add

* Descriptive Name: MyVPN-CA

* Method: Create an internal Certificate Authority

* Fill in Country, Org, Email etc.

Click **Save**.

![Cyber lab image](../Assets/Module%202/2.3.png)

---

### **Step 3: Create a VPN Server Certificate**

System \> Cert. Manager \> Certificates \> Add/Sign

* Descriptive Name: MyVPN-Server

* Method: Create internal Certificate

* Type: Server Certificate

* Choose CA: MyVPN-CA

Save.

![Cyber lab image](../Assets/Module%202/2.4.png)

---

### **Step 4: Create OpenVPN Server**

VPN \> OpenVPN \> Servers \> Add

* Server Mode: **Remote Access (User Auth)**

* Protocol: **UDP**

* Port: 1194

* Tunnel Network: 10.10.10.0/24

* Local Network: 10.0.0.0/24 (your LAN)

* Certificate: MyVPN-Server

* Auth: Username \+ Password (Local)

* Compression: Adaptive

* DNS: Enter Pi-hole IP

Save and apply.

![Cyber lab image](../Assets/Module%202/2.5.png)

---

### **Step 5: Add Firewall Rule for VPN**

Go to:

Firewall \> Rules \> WAN \> Add

* Protocol: UDP

* Destination Port Range: 1194

* Action: Pass

![Cyber lab image](../Assets/Module%202/2.6.png)
Save and apply.

---

### **Step 6: Add VPN User**

System \> User Manager \> Add

* Username: vpnuser1

* Password: securePassword

* Click: Create Certificate

* Certificate Authority: MyVPN-CA

* Save

---

### **Step 7: Export VPN Configuration**

Go to:

VPN \> OpenVPN \> Client Export

* Choose user

* Download installer .ovpn config file or Windows EXE

![Cyber lab image](../Assets/Module%202/2.7.png)
You can now connect securely from any device using **OpenVPN Client**.

![Cyber lab image](../Assets/Module%202/2.8.png)

---

##  **DNS Redirection to Pi-hole**

### **Step 1: Go to Firewall \> NAT \> Port Forward**

* Interface: LAN

* Protocol: TCP/UDP

* Source: any

* Destination Port: 53

* Redirect to: Pi-hole IP (e.g., 10.0.0.5)

* Redirect Port: 53  
![Cyber lab image](../Assets/Module%202/2.11.png)

This forces all devices to use Pi-hole as DNS.

---
![Cyber lab image](../Assets/Module%202/2.12.png)
## ** Logging & Monitoring**

* pfSense logs can be forwarded to **Splunk**

Go to:  
Status \> System Logs \> Settings

*  Enable remote syslog and point to your Splunk listener IP \+ port.

---

##  **Summary**

| Feature | Status |
| ----- | :---- |
| pfSense Installed | ✅ |
| Gateway Routing Setup | ✅ |
| Firewall Rules | ✅ |
| Time-Based Scheduling | ✅ |
| OpenVPN with CA | ✅ |
| Client Export Installed | ✅ |
| DNS to Pi-hole | ✅ |
