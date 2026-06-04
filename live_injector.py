from dotenv import load_dotenv
load_dotenv()

import os
import time
import random
from datetime import datetime
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_URI environment variable not set.")

client = MongoClient(MONGO_URI)
db = client["microgrid_network"]
collection = db["historical_telemetry"]

print("⚡ Initiating Live Microgrid Telemetry Stream...")
print("Press Ctrl+C to terminate.")

try:
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        
        # Baseline Normal Operating Data
        load_1, pv_1 = random.uniform(100, 150), random.uniform(90, 140)
        load_2, pv_2 = random.uniform(400, 500), random.uniform(380, 480)
        load_3, pv_3 = random.uniform(1700, 1900), random.uniform(1600, 1800)

        # CHAOS ENGINE: 10% chance to simulate an FDIA attack on Microgrid3
        is_attack = random.random() < 0.10
        if is_attack:
            print(f"\n[{now}] ⚠️ CHAOS ENGINE: INJECTING FDIA ANOMALY INTO MICROGRID3!")
            pv_3 = random.uniform(400, 850) # Drastically drop PV to simulate sensor spoofing

        mock_data = [
            {"microgrid_id": "Microgrid1", "timestamp": now, "load_kw": round(load_1, 2), "pv_kw": round(pv_1, 2), "type": "Residential"},
            {"microgrid_id": "Microgrid2", "timestamp": now, "load_kw": round(load_2, 2), "pv_kw": round(pv_2, 2), "type": "Commercial"},
            {"microgrid_id": "Microgrid3", "timestamp": now, "load_kw": round(load_3, 2), "pv_kw": round(pv_3, 2), "type": "Industrial"}
        ]

        collection.insert_many(mock_data)
        
        if not is_attack:
            print(f"[{now}] Telemetry synced to MongoDB Atlas.")
            
        time.sleep(3) # Wait 3 seconds before next telemetry ping

except KeyboardInterrupt:
    print("\nTelemetry Stream Terminated by Operator.")