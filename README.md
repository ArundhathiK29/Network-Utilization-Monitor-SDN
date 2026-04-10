# Network Utilization Monitor using SDN

## 📌 Aim
To measure and display bandwidth utilization across a network using Software Defined Networking (SDN) by collecting byte counters, estimating bandwidth usage, and updating results periodically.

---

## 🛠 Tools Used
- Ubuntu Virtual Machine
- Mininet Network Emulator
- POX SDN Controller
- Python 3

---

## 🌐 Network Topology
Single switch topology with 3 hosts:

h1 ---\
h2 ---- s1 ---- Controller (POX)
h3 ---/

---

## ⚙️ Setup & Execution

### Start Controller
```bash
cd ~/pox
python3 pox.py forwarding.l2_learning monitor
