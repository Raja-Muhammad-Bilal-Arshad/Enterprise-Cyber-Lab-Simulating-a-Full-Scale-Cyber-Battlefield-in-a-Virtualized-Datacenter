## **Module 9 – Secure Remote Access with ZeroTier**

### **Overview**

This module demonstrates the use of **ZeroTier**, a software-defined networking (SDN) solution, to create a **secure, encrypted overlay network** for remote access to the NUCFD Pentesting Lab.

By integrating **Proxmox**, **laptops**, and **mobile devices** into a private ZeroTier network:

* You can securely manage your infrastructure from **anywhere in the world**.

* **No port forwarding** is required, eliminating a common security risk.

* Devices communicate over **end-to-end encrypted tunnels** with **static IP assignments** for reliability.

---

### **Benefits**

| Feature | Advantage |
| :---- | :---- |
| **Global Access** | Manage your Proxmox datacenter from any location without VPN complexity. |
| **No Port Forwarding** | Removes exposure of management interfaces to the internet. |
| **Static IP Addresses** | Ensures predictable network paths for scripts and monitoring. |
| **Multi-Device Support** | Connect mobile, laptop, and servers to the same virtual LAN. |
| **Cross-Platform** | Works on Linux, Windows, macOS, iOS, Android, and embedded devices. |

---
![Cyber lab image](../Assets/Module%209/9.1.png)

### **Architecture**

**ZeroTier Virtual Network (10.147.17.0/24 in this example)**

* **Proxmox Datacenter Node:** `10.147.17.100`

* **Laptop:** `10.147.17.101`

* **Mobile Phone:** `10.147.17.102`

All devices are connected as if they were on the same local LAN, regardless of their physical location or ISP.

---

### **Step-by-Step Deployment**

#### **1\. Create a ZeroTier Account**

1. Visit https://www.zerotier.com and sign up for a free account.

2. Log in to the **My Networks** dashboard.
![Cyber lab image](../Assets/Module%209/9.2.png)
---

#### **2\. Create a Virtual Network**

1. In the dashboard, click **Create a Network**.

2. Copy the **Network ID** (e.g., `8056c2e21c000001`).

3. Optionally, set an IP range (e.g., `10.147.17.0/24`) under **Advanced Settings**.

4. Enable **Private Network** (recommended for security).

---

#### **3\. Install ZeroTier on All Devices**

**On Proxmox Host (Debian/Ubuntu base)**

```bash  
curl -s https://install.zerotier.com | sudo 
```

* (For Proxmox Do not write sudo because it do not support sudo)  
* **On Laptop (Windows/macOS/Linux)**  
   Download and install from https://www.zerotier.com/download/

* **On Mobile (iOS/Android)**  
   Install **ZeroTier One** from App Store or Google Play.

---

#### **4\. Join the Network**

On each device, run:

```bash  
`sudo zerotier-cli join <Network_ID>`
```
Example:

```bash  
`sudo zerotier-cli join 8056c2e21c000001`
```
---

![Cyber lab image](../Assets/Module%209/9.3.png)

#### ** Authorize Devices**

1. Go to the **ZeroTier Web Dashboard**.

2. Under your network, **approve each device** by ticking the checkbox.

3. Assign a **static IP** for each device to ensure predictable access.

![Cyber lab image](../Assets/Module%209/9.4.png)

---

#### **6\. Verify Connectivity**

From your laptop or mobile, ping your Proxmox datacenter:

```bash
`ping 10.147.17.100`
```

![Cyber lab image](../Assets/Module%209/9.5.png)

You should get replies even if both devices are on different physical networks.

---

#### **7\. Secure Proxmox Web Access**

1. In **Proxmox Firewall** or **Datacenter Firewall**, allow access **only** from your ZeroTier subnet.

2. Access Proxmox UI using:  
   ```bash  
   `https://10.147.17.100:8006`
   ```

3. Login and manage your datacenter securely.

---

### **Security Best Practices**

* **Keep ZeroTier private** – never make your network public.

* Assign **static IPs** to avoid accidental IP changes.

* Use **Proxmox firewall rules** to restrict access only to ZeroTier addresses.

* Enable **MFA** for your Proxmox login.

* Keep **ZeroTier client updated** on all devices.

---

### **Example Use Case**

While traveling:

* You open the ZeroTier app on your mobile phone.

* Connect to your secure ZeroTier network.

* Access the Proxmox datacenter UI on `10.147.17.100`.

* Manage, start, or stop VMs as if you were physically in your lab.
