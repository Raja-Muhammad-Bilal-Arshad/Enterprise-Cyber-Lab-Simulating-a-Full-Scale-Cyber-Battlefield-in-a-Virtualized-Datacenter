##  **Module 4: Centralized Logging & SIEM with Splunk**

**Objective:**  
 Enable deep packet and log analysis across all devices (Proxmox nodes, pfSense, Suricata/Snort alerts, OpenVPN logs, etc.) using **Splunk** for centralized log aggregation, real-time alerting, and visual dashboards.
 
 ![Cyber lab image](../Assets/Module%204/4.1.png)

 **Step-by-Step Instructions**

---

### **Step 1: Deploying Splunk in LXC(I made it inside a Ubuntu Server)**

####  **LXC Container Setup (Proxmox)**

1. Create an Ubuntu 22.04 LXC container

2. Assign a static IP (e.g. `192.168.1.250`)

3. Allocate:

   *  2 CPUs

   *  4–6 GB RAM

   *  40+ GB Disk

4. SSH into the container

---
![Cyber lab image](../Assets/Module%204/4.2.png)

###  **Step 2: Install Splunk Enter (Free Edition )**

```bash  
`# Download Splunk (adjust version as needed)`  
`wget -O splunk-9.deb 'https://download.splunk.com/products/splunk/releases/9.2.1/linux/splunk-9.2.1-dd0128b6e5cf-linux-2.6-amd64.deb'`

`# Install`  
`sudo dpkg -i splunk-9.deb`

`# Start & Accept license`  
`sudo /opt/splunk/bin/splunk start --accept-license`

`# Enable Splunk to start on boot`  
`sudo /opt/splunk/bin/splunk enable boot-start`

```

---
![Cyber lab image](../Assets/Module%204/4.3.png)

###  ** Step 3: Access Splunk Web Interface**

* Go to `http://192.168.1.250:8000`

* Default credentials:

  *  `admin`

  *  Create password during first login

![Cyber lab image](../Assets/Module%204/4.4.png)

---

###  **Step 4: Configure Data Inputs**

From the Splunk Web Dashboard:

1. Go to `Settings` → `Data Inputs`  
![Cyber lab image](../Assets/Module%204/4.5.png)

![Cyber lab image](../Assets/Module%204/4.6.png)

3. Add these inputs:

   *  **UDP 514** for pfSense Syslog

   *  **TCP 9997** for Universal Forwarder (if used)

   *  **Custom port** for Suricata/Snort logs

![Cyber lab image](../Assets/Module%204/4.7.png)

---

###  **Step 5: Forward Logs from pfSense**

#### **On pfSense:**

1. Go to `Status` → `System Logs` → `Settings`

2. Set:

   * Remote Syslog server: `192.168.1.250`

   * Remote syslog port: `514`

   * Transport: `UDP`

   * Facilities: `System`, `Firewall`, `OpenVPN`, `DNS Resolver`, etc.

 Now pfSense will send logs in real-time to Splunk

![Cyber lab image](../Assets/Module%204/4.8.png)

---

###  **Step 6: Forward Suricata/Snort Alerts**

1. Go to Suricata/Snort Interface settings

2. Enable:

   *  Unified2 format (or Syslog output)

   *  EVE JSON format (if supported)

3. Use rsyslog to forward alerts:
   
```bash
#Example for Suricata EVE JSON logs  
sudo nano /etc/rsyslog.d/60-suricata.conf

#Add: 
 @192.168.1.250:514 
 
 ```
4.Restart rsyslog:

   
```bash

sudo systemctl restart rsyslog 

```

![Cyber lab image](../Assets/Module%204/4.9.png)

---

###  **Step 7: Create Dashboards & Alerts**

1. In Splunk, go to **Search & Reporting**

Use queries like:


```bash  
 index=syslog sourcetype=pfSense | stats count by src_ip, dest_ip, action
```

2. Create dashboards for:

   *  Top attackers

   *  Blocked countries

   *  Suricata/Snort alerts

   *  VPN login attempts

---

###  **Bonus: Install TA-pfSense or TA-Snort App**

1. Go to `Manage Apps` → `Browse More Apps`

2. Search:

   * `TA-pfSense`

   * `TA-Snort`

   * `Splunk Dashboard Examples`

3. Install for cleaner fields and parsing

![Cyber lab image](../Assets/Module%204/4.10.png)

![Cyber lab image](../Assets/Module%204/4.11.png)

---

## **Summary**

| Source | Destination | Protocol | Port |
| :---- | :---- | :---- | :---- |
| pfSense Logs | Splunk LXC | UDP | 514 |
| Suricata | Splunk LXC | UDP/TCP | 514+ |
| OpenVPN Logs | Splunk Dashboard | Syslog | 514 |

 You now have **centralized real-time visibility** of all activity on your enterprise network.

---

Now , Brother this setup gives you a **SOC-in-a-box** inside your lab.
