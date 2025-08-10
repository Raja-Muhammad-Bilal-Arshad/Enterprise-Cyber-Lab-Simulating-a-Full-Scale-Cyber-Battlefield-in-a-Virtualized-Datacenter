# **Module 7: Centralized SIEM with Splunk**

## **Overview**

This module sets up a **centralized Security Information and Event Management (SIEM)** system using **Splunk** to collect, analyze, and alert on network security logs from multiple sources — including **pfSense firewall**, **DHCP server**, and **Suricata IDS/IPS**. The goal is to provide real-time visibility, detect threats, and improve incident response for enterprise networks.

---

## **Step-by-Step Guide to Setup and Use**

### **Step 1: Prepare Your Environment**

* Install **Splunk Enterprise** or **Splunk Free** on a dedicated monitoring server.  
   Official Splunk download: https://www.splunk.com/en\_us/download/splunk-enterprise.html

* Ensure your network devices (pfSense, DHCP, Suricata) can communicate with the Splunk server over the network.

* Basic Linux sysadmin knowledge is required to configure forwarding and Splunk inputs.  
![Cyber lab image](../Assets/Module%207/7.1.png)

---

### **Step 2: Configure Log Forwarding on Network Devices**

#### **2.1 Configure pfSense to Forward Logs**

* In pfSense Web GUI:

  * Go to **Status \> System Logs \> Settings**

  * Enable **Remote Logging**

  * Add your Splunk server IP and select **UDP** or **TCP** on port 514 (default syslog port)

  * Save and apply changes

* pfSense will now send firewall logs, block events, and alerts to Splunk.

#### **2.2 Configure DHCP Server Logs**

* If using Linux DHCP server (e.g., ISC DHCP):

  * Configure syslog to forward DHCP logs to Splunk server.

Example in /etc/rsyslog.conf or /etc/syslog.conf:

```bash  
local7.\*   @splunk-server-ip:514
```

Restart syslog service:  
```bash  
sudo systemctl restart rsyslog
```

* If using Windows DHCP server, configure Windows Event Forwarding or export logs for Splunk ingestion.

#### **2.3 Configure Suricata IDS/IPS**

Enable **EVE JSON output** in Suricata config /etc/suricata/suricata.yaml:  
```bash  
outputs:  
  \- eve-log:  
      enabled: yes  
      filetype: regular  
      filename: /var/log/suricata/eve.json  
      types:  
        \- alert  
        \- dns  
        \- http  
        \- tls
```

* Configure Splunk to monitor the eve.json file for real-time alerts.

---

### **Step 3: Configure Splunk Data Inputs**

* Login to Splunk Web UI: http://\<splunk-server-ip\>:8000

* Go to **Settings \> Data Inputs**

* Add inputs for:

  * **UDP/TCP Syslog** on port 514 (to receive pfSense and DHCP logs)

  * **File monitoring** for Suricata’s eve.json

* Define source types and index (e.g., pfsense\_logs, dhcp\_logs, suricata\_alerts) for easy filtering.
  

![Cyber lab image](../Assets/Module%207/7.2.png)

---

### **Step 4: Build and Import Dashboards**

* Create custom Splunk dashboards to visualize:

  * Firewall traffic and block events

  * DHCP IP lease activity and conflicts

  * Suricata alerts categorized by severity and type

* You can export dashboards as JSON and share or import into other Splunk instances.

---

### **Step 5: Automated Alerting**

* Configure alert rules in Splunk to trigger on:

  * High-severity Suricata intrusion alerts

  * Repeated firewall blocks from suspicious IPs

  * DHCP anomalies or unexpected IP conflicts

* Alerts can send email, Slack messages, or trigger webhook actions for SOC teams.

---

### **Step 6: Integrate Python Socket Application Monitoring (Optional)**

* Modify your Python pentesting and socket tools to send logs or metrics to Splunk.  
   Options include:

  * Writing logs to syslog (forwarded to Splunk)

  * Sending logs to Splunk HTTP Event Collector (HEC)

* This provides full visibility of custom tool activity within the SIEM.

---

## **How IDS/IPS (Suricata) Responds**

* Suricata analyzes network traffic in real-time and logs detected suspicious activity as **alerts** in eve.json.

* Splunk monitors this log file continuously, indexing alerts for search and visualization.

* When a critical alert is detected (e.g., port scan, brute force attempt), Splunk’s alerting system notifies admins immediately.

* This feedback loop enables proactive response to potential threats.

---

## **Summary Diagram**

```yaml  
\[pfSense Firewall\] \------\>   
\[DHCP Server\] \-----------|   
\[Suricata IDS/IPS\] \------\> \[Splunk Server\] \--\> Dashboards & Alerts  
                                ↑  
                                |  
                      \[Python Socket Tools Logs\]
```

---

## **Troubleshooting Tips**

* Ensure Splunk is reachable from all devices on the required ports.

* Check firewalls and ACLs are not blocking syslog or file forwarding traffic.

* Verify Suricata’s eve.json is being updated in real-time.

* Use Splunk search queries to confirm logs are ingested properly.  
![Cyber lab image](../Assets/Module%207/7.3.png)

---

## **Additional Resources**

* https://docs.splunk.com/Documentation  
* https://docs.netgate.com/platforms/  
* https://docs.suricata.io/en/latest/output/eve/eve-json-format.html

---

## **Author**

# *Raja Muhammad Bilal*
