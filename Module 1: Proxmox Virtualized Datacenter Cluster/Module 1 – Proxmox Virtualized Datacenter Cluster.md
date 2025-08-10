#  **Module 1 – Proxmox Virtualized Datacenter Cluster**

### ***Setting up the Foundation of an Enterprise-Grade Network***

---

##  **What This Module Does**

This module sets up a **3-node Proxmox Virtual Environment (PVE) Cluster**, forming the **core of your enterprise network infrastructure**. Clustering allows multiple Proxmox nodes to act as one logical unit — enabling:

* Centralized management

* Resource balancing

* Future high-availability (HA) support

* Modular node roles (e.g., gateway, SIEM, WAN simulation)
    
![Cyber lab image](../Assets/Module%201/1.1.png)

---

##  **Infrastructure Topology**

  Proxmox3                              Proxmox1                             Proxmox2             
  WAN Sim               ───►    Gateway            ───►        SIEM                

| Node | Role | RAM | Storage |
| ----- | ----- | ----- | ----- |
| Proxmox1 | Gateway \+ Firewall \+ Pi-hole | 2–4 GB | 100 GB |
| Proxmox2 | Splunk \+ SIEM Monitoring | 6 GB | 400 GB |
| Proxmox3 | WAN Traffic Simulation | 2 GB/node | 100 GB/node |

---

##  **How Proxmox Clustering Works**

A **Proxmox Cluster** uses the corosync service to sync configuration and allow seamless centralized control.

**Key Concepts:**

* The **master node** creates the cluster

* Other nodes **join the cluster** using the master's IP and a generated token

* Nodes **must be on the same subnet** and have **unique hostnames**

![Cyber lab image](Assets/Module 1/1.2.png)

---

##  **Method 1: Create & Join Cluster via Web GUI**

### **Step 1: Create the Cluster (on Proxmox1)**

1. Go to: Datacenter \> Cluster

2. Click: Create Cluster

3. Fill in:

   * **Cluster Name**: EnterpriseLab (or your choice)

   * **Network Interface**: vmbr0 (or whichever your LAN uses)

4. Click Create

###  **Step 2: Join Another Node (e.g., Proxmox2/3)**

1. Go to: Datacenter \> Cluster (on new node)

2. Click: Join Cluster

3. Paste:

   * **Cluster Join Info** (you can copy this from the master node)

   * Enter the **root password** of the master

4. Click Join

###  **Step 3: Reboot the node (if prompted)**

![Cyber lab image](Assets/Module 1/1.3.png)

---

##  **Method 2: Cluster Setup via Terminal (Advanced)**

###  **Step-by-Step Commands**

####  **On Master Node (Proxmox1):**

```bash  
\# Set hostname  
hostnamectl set-hostname proxmox1

\# Add entries to /etc/hosts (IMPORTANT)  
nano /etc/hosts  
\# Add:  
192.168.1.101 proxmox1  
192.168.1.102 proxmox2  
192.168.1.103 proxmox3

\# Create the cluster  
pvecm create EnterpriseLab \--bindnet0 192.168.1.0

```

**On Joining Node (Proxmox2/Proxmox3):**

```bash  
\# Set hostname  
hostnamectl set-hostname proxmox2

\# Edit /etc/hosts  
nano /etc/hosts  
\# Same as above — include all node IPs and names

\# Join cluster (replace IP with master node’s IP)  
pvecm add 192.168.1.101

```  
**Check Cluster Status:**  
```bash  
pvecm status  
```

You should see your nodes listed with their quorum status and vote count.

## **Tips & Best Practices**

* Make sure **NTP is enabled** on all nodes (timedatectl status)

* Use **static IPs** on all Proxmox nodes

* Ensure **firewalls allow port 22 (SSH)** and **port 8006 (Web UI)**

* If issues occur, restart corosync:  

   ```bash
    systemctl restart corosync
   ```



## **Summary**

* Set hostnames and IPs properly

* Master node creates the cluster

* Other nodes join via Web GUI or CLI

* You now have a **clustered enterprise platform ready for advanced deployments**

![Cyber lab image](Assets/Module 1/1.4.png)

