import requests

from coordinator.monitor import AvailabilityMonitor

API_URL = "http://localhost:8080/data"

def run_test_suite(mode_name):
    print(f"\n--- Testing Mode: {mode_name} ---")
    successes = 0
    total = 5
    
    for i in range(total):
        try:
            r = requests.post(API_URL, 
                             json={"key": f"test_{i}", "value": "data"}, 
                             timeout=1)
            if r.status_code == 200:
                successes += 1
                print(f"Request {i+1}: Success")
            else:
                print(f"Request {i+1}: Failed (SLA Breach)")
        except Exception as e:
            print(f"Request {i+1}: Error ({e})")
            
    print(f"SLA Status: {(successes/total)*100}% Success Rate")

def test_three_nines_threshold(manager):
    # simulate a stable system (999 successes)
    manager.total_requests = 1000
    manager.successful_requests = 1000 
    
    # trigger one failure to hit strong wall, perform a strong write while a node is down
    manager.total_requests += 1
    # successful_requests stays at 1000
    
    uptime = manager.get_uptime_percentage() # returns 99.9000...
    status = manager.get_sla_status()
    
    print(f"Uptime: {uptime}% | Status: {status}")
    assert status == "3 Nines (Standard)"

# run the following scenarios separately
# 1) run with all 3 nodes up
# 2) run 'docker stop node-3' and run again
# 3) run 'docker stop node-2' and run again
run_test_suite("CURRENT_MODE")

print()

# test three nines threshold
test_three_nines_threshold(AvailabilityMonitor())