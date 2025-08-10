## **Module 3: Inline Network Security with Suricata, Snort & pfBlockerNG in pfSense**

---

###  **Overview**

In this module, we transform pfSense into a powerful unified threat management device by integrating:

* **Suricata** – An open-source IDS/IPS with rich rule support.

* **Snort** – Cisco’s signature-based packet analyzer.

* **pfBlockerNG** – Country/IP/DNS filtering firewall enhancement.

These tools monitor, detect, and block malicious traffic in real-time across WAN/LAN interfaces with minimal resource consumption.

---

##  **Step-by-Step Installation**

###  **Step 1: Install Packages from pfSense GUI**

####  **Navigate:**

`System` → `Package Manager` → `Available Packages`

####  **Install:**

*  **Suricata**

*  **Snort**

*  **pfBlockerNG-devel** (Important: Use `devel` version)

Each will appear under `Services` after install.

![Cyber lab image](../Assets/Module%203/3.1.png)

---

##  **Step 2: Suricata Setup**

###  **Add Interface**

1. Go to `Services` → `Suricata`

2. Click `+ Add`

3. Select **LAN** or **WAN** as interface

4. Choose:

   *  `IPS Mode`: **Enabled**

   *  `Pattern Matcher`: Aho-Corasick

   *  `Block Offenders`: Enabled

   *  `Block Drops`: Enabled
![Cyber lab image](../Assets/Module%203/3.2.png)

### **Rule Management**

1. Under the `Global Settings` tab:

   * Enable automatic rule updates

   * Select `ET Open Rules` or upload custom rules

2. Click `Update Rules` to download

###  **Enable Interface (Legacy / IPS Mode)**

* Go to `Interface Settings`

* Enable:

  *  **Promiscuous Mode**

  *  **Block Offenders**

  *  **IPS Mode (Legacy or Inline)**

 **Legacy Mode**: IDS-style, logging only  
 **Inline (Unblock Mode)**: Full IPS, actively blocks threats

 On pfSense, **Legacy Mode** means detection only  
  **IPS Mode (Inline)** means Suricata acts like a firewall rule

---

##  **Step 3: Snort Setup**

###  **Add Interface**

1. Go to `Services` → `Snort`

2. Click `+ Add`

3. Choose LAN or WAN

4. Settings:

   *  `Block Offenders`

   *  `Enable Rules`

   *  `Download Snort VRT rules` (Register on Snort website and enter Oinkcode)
![Cyber lab image](../Assets/Module%203/3.3.png)
### ** Enable Rule Updates **

1. Go to `Global Settings`

2. Enable:

   * `Snort Community Rules`

   * `Snort VRT Rules`

   * `ET Open Rules`

3. Apply updates

 Don’t enable Suricata and Snort on the same interface at the same time – choose one for each.

![Cyber lab image](../Assets/Module%203/3.4.png)

---

##  **Step 4: pfBlockerNG Setup**

###  **Initial Setup Wizard**

1. Go to `Firewall` → `pfBlockerNG`

2. Run **Setup Wizard**

   * Choose:

     * `WAN` as inbound

     * `LAN` as outbound

     * Block both IPv4 and IPv6 (optional)  
![Cyber lab image](../Assets/Module%203/3.5.png)
![Cyber lab image](../Assets/Module%203/3.6.png)

###  **GeoIP Blocking**

1. Go to `IP` → `GeoIP`

2. Enable:

   * `Deny Inbound` for countries (e.g., block CN, RU, KP)

   * `Deny Outbound` (optional)

3. Choose the countries

4. Save & Apply  
![Cyber lab image](../Assets/Module%203/3.7.png)

###  **DNSBL (Ad/Malware Blocking)**

1. Go to `DNSBL` tab

2. Enable DNSBL

3. Add lists (e.g., EasyList, malware domains, social media)

4. Apply changes

---

##  **Final Activation**

After all configuration:

* Go to `Update` tab in pfBlockerNG

* Run **Force Update**

![Cyber lab image](../Assets/Module%203/3.8.png)

---

##  **Testing IDS/IPS**

Use a known test site to generate alerts:

`curl http://testmyids.com`

Check logs under:

* `Status` → `System Logs` → `Suricata` or `Snort`

* pfBlockerNG → Reports → IP / DNSBL

---

##  

## **Summary**

| Tool | Function | Interface | Mode |
| ----- | ----- | ----- | ----- |
| Suricata | IDS/IPS | LAN/WAN | Inline/Legacy |
| Snort | IDS | WAN | Detection |
| pfBlockerNG | Firewall Filter | WAN/LAN | Country/IP/DNS |

---

Your pfSense is now a **Layer-7 Firewall with inline threat prevention** and **blocklists** for privacy and security.
