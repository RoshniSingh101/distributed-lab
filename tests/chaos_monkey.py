import docker
import time
import random

client = docker.from_env()
nodes = ["node-1", "node-2", "node-3"]

def chaos():
    print("🚀 Chaos Monkey started. Breaking things...")
    while True:
        target = random.choice(nodes)
        print(f"🔥 Killing {target}...")
        try:
            container = client.containers.get(target)
            container.stop()
            
            time.sleep(10) # Leave it down for 10 seconds
            
            print(f"✅ Recovering {target}...")
            container.start()
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(random.randint(5, 15))

if __name__ == "__main__":
    chaos()