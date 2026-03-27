import requests
import threading

NODES = ["http://node-1:8000", "http://node-2:8000", "http://node-3:8000"]

class ConsistencyManager:
    @staticmethod
    def write_strong(key, value):
        """CP Mode: All nodes must acknowledge the write."""
        success_count = 0
        
        for node in NODES:
            try:
                # short timeout to prevent hanging the dashboard
                r = requests.post(f"{node}/set", json={"key": key, "value": value}, timeout=0.2)
                if r.status_code == 200:
                    success_count += 1
            except Exception:
                # if one node is down, we stop and fail immediately
                print(f"Strong Write Failed: Node {node} is unreachable.")
                return False 

        # return True only if every single node responded
        return success_count == len(NODES)

    @staticmethod
    def write_eventual(key, value):
        """AP Mode: Write to the first available node, sync others in background."""
        primary_success = False
        target_node = None

        # find at least one node to take the data immediately
        for node in NODES:
            try:
                # short timeout is key to prevent hanging on dead nodes
                r = requests.post(f"{node}/set", json={"key": key, "value": value}, timeout=0.2)
                if r.status_code == 200:
                    primary_success = True
                    target_node = node
                    break # "First Responder" found
            except Exception:
                continue # try the next node in the list

        # if no nodes are alive at all, then return false
        if not primary_success:
            return False

        # async background sync to the remaining nodes
        def sync():
            for node in NODES:
                if node == target_node:
                    continue # skip the one wrote to
                try:
                    requests.post(f"{node}/set", json={"key": key, "value": value}, timeout=0.5)
                except Exception:
                    pass # in eventual, ignore if background sync fails now

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
            except Exception:
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
                    return True # success on active node
            except Exception:
                print("Node failing, attempting failover...")
                continue # try the passive node
                
        return False # return false if both nodes are down