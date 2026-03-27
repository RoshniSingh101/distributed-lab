import requests
import threading

NODES = ["http://node-1:8000", "http://node-2:8000", "http://node-3:8000"]

class ConsistencyManager:
    @staticmethod
    def write_strong(key, value):
        """CP (consistency and partition tolerance) Mode: Must write to ALL nodes to succeed."""
        responses = []
        for node in NODES:
            try:
                r = requests.post(f"{node}/set", json={"key": key, "value": value}, timeout=1)
                responses.append(r.status_code)
            except:
                responses.append(500)
        
        # If any node failed, a 'Strong' system technically has a consistency issue
        return all(res == 200 for res in responses)

    @staticmethod
    def write_eventual(key, value):
        """AP (availability and partition tolerance) Mode: Write to one, sync others in background."""
        # Write to the first available node immediately
        requests.post(f"{NODES[0]}/set", json={"key": key, "value": value})
        
        # Async background sync to others (Eventual)
        def sync():
            for node in NODES[1:]:
                requests.post(f"{node}/set", json={"key": key, "value": value})
        
        threading.Thread(target=sync).start()
        return True
    
    @staticmethod
    def write_quorum(key, value, required_nodes=2):
        """
        Quorum Mode: Success if a MAJORITY of nodes respond.
        Provides a balance of Consistency and Availability.
        """
        success_count = 0
        for node in NODES:
            try:
                r = requests.post(f"{node}/set", json={"key": key, "value": value}, timeout=0.5)
                if r.status_code == 200:
                    success_count += 1
            except:
                continue
        
        return success_count >= required_nodes
    
    @staticmethod
    def write_active_passive(key, value):
        """
        Failover Pattern: Try Node 1. If it fails, failover to Node 2.
        """
        nodes_to_try = ["http://node-1:8000", "http://node-2:8000"]
        
        for node in nodes_to_try:
            try:
                r = requests.post(f"{node}/set", json={"key": key, "value": value}, timeout=0.5)
                if r.status_code == 200:
                    return True # Success on Active node
            except:
                print(f"Node failing, attempting failover...")
                continue # Try the Passive node
                
        return False # Both nodes are down