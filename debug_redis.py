import time

import redis

r = redis.Redis(host="localhost", port=6379, db=0)
print("Setting test key...")
try:
    r.set("test-key", "working")
    print(f"Test key value: {r.get('test-key')}")
except Exception as e:
    print(f"Error connecting: {e}")

print("Checking kiln-pv...")
for i in range(5):
    val = r.get("kiln-pv")
    print(f"Attempt {i}: {val}")
    time.sleep(1)
