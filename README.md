# Distributed Systems Lab: Consistency & Fault Tolerance

A Python and JavaScript-based distributed key-value store designed to demonstrate the trade-offs between **Consistency** and **Availability** (the CAP Theorem). This system features a central Coordinator, three worker Nodes, and a real-time SLA Monitoring Dashboard.

---

## Quick Start

### 1. Launch the Cluster
```bash
# Build and start the 3 nodes + coordinator + dashboard
docker-compose up -d --build
```

### 2. Access the Dashboard
Open your browser to http://localhost:8080 to see the real-time SLA monitor.

### 3. Simulate a Fault
```bash
# Kill a specific node (1, 2, or 3) to test Quorum vs. Strong consistency
docker stop node-1
```

### Project Structure
* /coordinator: Flask API managing consistency logic and SLA tracking
* /nodes: Lightweight Python workers storing key-value pairs
* /frontend: Vanilla JS dashboard using CSS Grid and real-time health checks
* docker-compose.yml: Orchestrates the 4-container network
  
---
## Technical Architecture

### 1. Consistency Modes
The system implements three distinct consistency strategies managed by the `ConsistencyManager`:

* **STRONG (CP):** Requires all $N$ nodes (**3/3**) to acknowledge a write. If any node is down, the write fails to ensure total data integrity across the cluster.
* **QUORUM (Balanced):** Requires a majority ($\lfloor N/2 \rfloor + 1 = \mathbf{2}$) of nodes. This provides fault tolerance while maintaining a high level of consistency.
* **EVENTUAL (AP):** Requires only **one** node to succeed immediately. The remaining nodes are synchronized via background threads to prioritize system uptime.


### 2. The SLA Monitor
The `AvailabilityMonitor` tracks every request and classifies system health based on uptime percentages. To handle lab-scale testing (100-request batches), the thresholds are:
* **5 Nines (Carrier Grade):** $\ge 99.999\%$ Uptime
* **3 Nines (Standard):** $\ge 99.9\%$ Uptime
* **Failing SLA:** $< 99.9\%$ Uptime

---
## Testing Fault Tolerance

We validate the implementation by running "Stress Tests" (100 concurrent writes) under different node health conditions:

### Case A: Healthy Cluster (3/3 Nodes Online)
* **Strong Mode:** 100% Success.
* **Quorum Mode:** 100% Success.
* **Result:** All modes achieve **5 Nines**.

### Case B: Degraded Cluster (2/3 Nodes Online)
* **Strong Mode:** **Failure.** The "Strong Wall" prevents writes because 3/3 consistency cannot be met. **SLA Status: Failing.**
* **Quorum Mode:** **Success.** Since 2/3 nodes are still online, the majority requirement is satisfied. **SLA Status: 3-5 Nines.**

**Result:** Demonstrates how Quorum maintains availability during partial partitions.

---
## Clean-Up
After you are satisfied with your cluster, CTRL+C in the terminal and run the following command.
```bash
# Build and start the 3 nodes + coordinator + dashboard
docker-compose down
```

