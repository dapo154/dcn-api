from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MongoDB Connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://testuser:testpass123@cluster0.inkdjrq.mongodb.net/dcn_network?retryWrites=true&w=majority&appName=Cluster0')
client = MongoClient(MONGODB_URI)
db = client.dcn_network

# Helper to convert ObjectId to string
def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# ==================== ROUTES ====================

@app.route('/')
def home():
    return jsonify({
        "message": "DCN Network API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    })

# GET all SIMs
@app.route('/api/sims', methods=['GET'])
def get_sims():
    sims = list(db.sims.find().limit(50))
    return jsonify([serialize_doc(sim) for sim in sims])

# GET single SIM by number
@app.route('/api/sims/<sim_number>', methods=['GET'])
def get_sim(sim_number):
    sim = db.sims.find_one({"sim_number": sim_number})
    if sim:
        return jsonify(serialize_doc(sim))
    return jsonify({"error": "SIM not found"}), 404

# POST activate SIM
@app.route('/api/sims/activate', methods=['POST'])
def activate_sim():
    data = request.json
    sim_number = data.get('sim_number')
    owner = data.get('owner')
    
    if not sim_number or not owner:
        return jsonify({"error": "sim_number and owner required"}), 400
    
    result = db.sims.update_one(
        {"sim_number": sim_number, "status": {"$in": ["inactive", "pending"]}},
        {"$set": {"status": "active", "owner": owner, "activated_at": datetime.now()}}
    )
    
    if result.modified_count > 0:
        return jsonify({"message": "SIM activated successfully", "sim_number": sim_number})
    return jsonify({"error": "SIM not found or already active"}), 400

# GET SIM stats
@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = db.sims.count_documents({})
    active = db.sims.count_documents({"status": "active"})
    inactive = db.sims.count_documents({"status": "inactive"})
    pending = db.sims.count_documents({"status": "pending"})
    
    return jsonify({
        "total_sims": total,
        "active": active,
        "inactive": inactive,
        "pending": pending
    })

# POST add to waitlist
@app.route('/api/waitlist', methods=['POST'])
def add_to_waitlist():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email required"}), 400
    
    existing = db.waitlist.find_one({"email": email})
    if existing:
        return jsonify({"message": "Already on waitlist"}), 200
    
    db.waitlist.insert_one({
        "email": email,
        "created_at": datetime.now(),
        "source": "landing_page"
    })
    
    return jsonify({"message": "Added to waitlist"}), 201

# GET waitlist count
@app.route('/api/waitlist/count', methods=['GET'])
def waitlist_count():
    count = db.waitlist.count_documents({})
    return jsonify({"count": count})

if __name__ == '__main__':
    print("🚀 DCN API starting...")
    print(f"📊 SIMs in DB: {db.sims.count_documents({})}")
    app.run(host='0.0.0.0', port=5000, debug=True)