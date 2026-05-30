import os
from pymongo import MongoClient

# Connect to MongoDB using your exported URI
MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_URI environment variable not set. Export it first!")

client = MongoClient(MONGO_URI)
db = client["microgrid_network"]
collection = db["historical_telemetry"]

# Define the mock telemetry data matching your topology
mock_data = [
    {"microgrid_id": "Microgrid1", "timestamp": "14:00", "load_kw": 120, "pv_kw": 115, "type": "Residential"},
    {"microgrid_id": "Microgrid2", "timestamp": "14:00", "load_kw": 450, "pv_kw": 410, "type": "Commercial"},
    {"microgrid_id": "Microgrid3", "timestamp": "14:00", "load_kw": 1800, "pv_kw": 850, "type": "Industrial"} # The target for our simulated attack
]

# Insert the data into MicrogridNexus
collection.delete_many({}) # Clear any old data
collection.insert_many(mock_data)
print("MicrogridNexus seeded successfully! Telemetry data is live.")