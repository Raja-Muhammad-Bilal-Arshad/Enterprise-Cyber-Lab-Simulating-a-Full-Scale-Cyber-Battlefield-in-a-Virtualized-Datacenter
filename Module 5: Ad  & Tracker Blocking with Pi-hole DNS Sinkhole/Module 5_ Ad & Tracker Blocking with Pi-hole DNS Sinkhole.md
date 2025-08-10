##  **Module 5: Ad & Tracker Blocking with Pi-hole DNS Sinkhole**

**Objective:**  
 Implement **network-wide ad blocking**, prevent **malware domains**, and **enhance privacy** by using **Pi-hole** as a local DNS server for all devices. Integrate it with pfSense for **complete DNS control**.

---

##  **Step-by-Step Instructions**

---

###  **Step 1: Deploy Pi-hole in an LXC on Proxmox**

####  **LXC Container Specs:**

* OS: Ubuntu 22.04

* Static IP: `10.10.16.46`

* Hostname: `pihole.local`

* Memory: 1–2 GB

* Disk: 10–15 GB

* CPU: 1 core

![Cyber lab image](../Assets/Module%205/5.1.png)

---

###  **Step 2: Install Pi-hole**

```bash  
`# Update packages`  
`sudo apt update && sudo apt upgrade -y`

`# Run the Pi-hole automated installer`  
`curl -sSL https://install.pi-hole.net | bash`  
```

 During the installation:

* Set static IP: `10.10.16.46`

* Upstream DNS: `Cloudflare (1.1.1.1)` or `Google (8.8.8.8)`

* Choose blocklists: Default is OK (can add more later)

* Web admin interface:  YES

* Log queries:  YES

* Privacy level: 0 (show everything) for debugging

---

###  **Step 3: Access Web Admin**

* URL: `http://10.10.16.46/admin`

Default login password shown at end of install (can reset using:

```bash  
````pihole -a -p```)````
```

![Cyber lab image](../Assets/Module%205/5.2.png)

---

###  **Step 4: Integrate Pi-hole with pfSense DNS**

####  **pfSense Settings**

1. Navigate to: `System` → `General Setup`

2. Set DNS servers:

   * DNS 1: `10.10.16.46`(your Pi-hole)

   * Uncheck: "Allow DNS server list to be overridden by DHCP/PPP on WAN"

3. Navigate to: `Services` → `DHCP Server`

4. Under `DNS Servers`:

   * Put only: `192.168.1.240`

Now all devices getting IPs from pfSense will use Pi-hole automatically.

![Cyber lab image](../Assets/Module%205/5.3.png)

---

###  **Step 5: Enable Conditional Forwarding (Optional)**

This allows Pi-hole to resolve local hostnames.

1. Go to Pi-hole Admin: `Settings` → `DNS`

2. Scroll to “Conditional Forwarding”

3. Enable and fill:

   * Local network IP range: e.g., `192.168.1.0/24`

   * pfSense IP (router): `10.10.16.20`

   * Local domain name: `home.local` (or your LAN domain)

![Cyber lab image](../Assets/Module%205/5.4.png)

---

###  **Step 6: Add Extra Blocklists**

Go to: `Group Management` → `Adlists`

Add high-quality lists like:

* StevenBlack

* Firebog

* Malware/Phishing/Tracking-specific lists

![Cyber lab image](../Assets/Module%205/5.5.png)

---

###  **Step 7: Test It\!**

Try browsing sites like:

* http://ads.google.com (should fail to load)

* http://speedtest.net (ads blocked)

Check query logs in Pi-hole dashboard:

*  Query Types

*  Blocked Domains

* Top Blocked

---

##  **Bonus: DNSSEC \+ DoH/DoT (Optional Hardening)**

* Enable DNSSEC in Pi-hole DNS settings.

* Use **Cloudflared** or **Stubby** to enable **DNS-over-HTTPS (DoH)** or **DNS-over-TLS (DoT)**.

---

###  **Summary Table**

| Component | Address | Role |
| ----- | ----- | ----- |
| Pi-hole | 10.10.16.46 | DNS sinkhole, ad blocker |
| pfSense | 10.10.16.20 | DHCP & DNS forwarder |
| Clients | via pfSense DHCP | Use Pi-hole as DNS |

---

 # **RESULT:**  
  Network-wide ad/tracker/malware blocking  
  Faster browsing & fewer annoyances  
  Less DNS leakage — more privacy\!
