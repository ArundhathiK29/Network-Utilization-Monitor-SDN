# 🚀 Network Utilization Monitor using SDN

## 📌 Aim
To measure and display bandwidth utilization across a network using Software Defined Networking (SDN) by collecting byte counters, estimating bandwidth usage, and updating results periodically.

---

## 🧠 Problem Statement
Traditional networks lack centralized visibility and dynamic monitoring. This project uses SDN to monitor real-time network utilization by collecting statistics from switches and computing bandwidth dynamically.

---

## 🛠️ Tools & Technologies
- Ubuntu Virtual Machine  
- Mininet (Network Emulator)  
- POX SDN Controller  
- Python 3  
- OpenFlow Protocol  

---

## 🌐 Network Topology

A simple single-switch topology with three hosts:


h1 ----

h2 ------ s1 -------- Controller (POX)
/
h3 ----/


---

## ⚙️ Working Principle

1. Mininet creates a virtual network with hosts and a switch  
2. POX controller connects to the switch using OpenFlow  
3. Controller requests port statistics (byte counters)  
4. Bandwidth is calculated using:


Bandwidth = (Current Bytes - Previous Bytes) / Time Interval


5. Results are displayed in real-time  

---

## ▶️ Execution Steps

### 1. Start Controller
```bash
cd ~/pox
python3 pox.py forwarding.l2_learning monitor
2. Start Mininet
sudo mn --controller=remote --topo single,3
3. Test Connectivity
pingall
4. Generate Traffic
h1 ping h2
iperf h1 h2
🔍 Flow Table Inspection

Flow rules installed in the switch can be viewed using:

sudo ovs-ofctl dump-flows s1
📸 Results & Outputs
🔹 Controller Running

🔹 Successful Ping Test

🔹 Flow Table Entries

🔹 Throughput Test (iperf)

🔹 High Traffic Monitoring

🔹 Idle Network State

🔹 Failure Scenario

🔹 Recovery Scenario

🧪 Test Scenarios
✅ 1. Normal Traffic
Low bandwidth usage observed during basic ping
✅ 2. High Traffic
iperf generates high throughput
Bandwidth values increase significantly
❌ 3. Failure Case
Link failure results in packet loss
🔄 4. Recovery
Network resumes normal operation after link restoration
✅ Validation
No traffic → bandwidth ≈ 0
Traffic present → bandwidth increases
Results consistent across multiple runs
📊 Performance Observations
Low latency observed in ping tests
High throughput during iperf tests
Flow tables confirm correct forwarding behavior
Real-time monitoring achieved successfully
🎯 Conclusion

This project successfully demonstrates how SDN enables centralized network monitoring. By leveraging the POX controller and Mininet, real-time bandwidth utilization was measured, analyzed, and displayed dynamically.
