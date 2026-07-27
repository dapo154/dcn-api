import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Load from .env or use direct connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://testuser:testpass123@cluster0.inkdjrq.mongodb.net/dcn_network?retryWrites=true&w=majority&appName=Cluster0')

def seed_sims():
    client = MongoClient(MONGODB_URI)
    db = client.dcn_network
    sims_collection = db.sims
    
    # Clear existing test data
    sims_collection.delete_many({"is_test": True})
    
    # Generate 20 test SIMs
    test_sims = []
    for i in range(1, 21):
        sim_number = f"DCN{random.randint(100000000, 999999999)}"
        sim = {
            "sim_number": sim_number,
            "iccid": f"8910300000{random.randint(1000000000, 9999999999)}",
            "status": random.choice(["active", "inactive", "pending"]),
            "plan": random.choice(["basic", "standard", "premium", "unlimited"]),
            "data_balance": random.choice([500, 1000, 2000, 5000, 10000]),  # MB
            "is_test": True,
            "created_at": datetime.now(),
            "activated_at": datetime.now() - timedelta(days=random.randint(0, 30)) if random.random() > 0.3 else None,
            "owner": None,
            "emergency_contacts": [],
            "mesh_node_id": f"node_{random.randint(100, 999)}"
        }
        test_sims.append(sim)
    
    result = sims_collection.insert_many(test_sims)
    print(f"✅ Seeded {len(result.inserted_ids)} test SIMs")
    
    # Show summary
    active_count = sims_collection.count_documents({"status": "active", "is_test": True})
    print(f"📊 Active: {active_count} | Inactive: {20 - active_count}")
    
    # Show first 3 SIMs
    print("\n📱 Sample SIMs:")
    for sim in sims_collection.find({"is_test": True}).limit(3):
        print(f"   {sim['sim_number']} | {sim['plan']} | {sim['data_balance']}MB | {sim['status']}")

if __name__ == "__main__":
    try:
        seed_sims()
        print("\n🚀 Ready to build DCN!")
    except Exception as e:
        print(f"❌ Error: {e}")