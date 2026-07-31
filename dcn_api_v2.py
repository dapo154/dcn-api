from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://testuser:testpass123@cluster0.inkdjrq.mongodb.net/dcn_network?retryWrites=true&w=majority&appName=Cluster0')
client = MongoClient(MONGODB_URI)
db = client.dcn_network

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@app.route('/')
def home():
    return jsonify({
        "message": "DCN Network API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/sims', methods=['GET'])
def get_sims():
    sims = list(db.sims.find().limit(50))
    return jsonify([serialize_doc(sim) for sim in sims])

@app.route('/api/sims/<sim_number>', methods=['GET'])
def get_sim(sim_number):
    sim = db.sims.find_one({"sim_number": sim_number})
    if sim:
        return jsonify(serialize_doc(sim))
    return jsonify({"error": "SIM not found"}), 404

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

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = db.sims.count_documents({})
    active = db.sims.count_documents({"status": "active"})
    inactive = db.sims.count_documents({"status": "inactive"})
    pending = db.sims.count_documents({"status": "pending"})
    waitlist = db.waitlist.count_documents({})
    
    return jsonify({
        "total_sims": total,
        "active": active,
        "inactive": inactive,
        "pending": pending,
        "waitlist_count": waitlist
    })

@app.route('/api/waitlist', methods=['POST'])
def add_to_waitlist():
    data = request.json
    email = data.get('email')
    
    if not email or '@' not in email:
        return jsonify({"error": "Valid email required"}), 400
    
    existing = db.waitlist.find_one({"email": email})
    if existing:
        return jsonify({"message": "Already on waitlist", "count": db.waitlist.count_documents({})}), 200
    
    db.waitlist.insert_one({
        "email": email,
        "created_at": datetime.now(),
        "source": "landing_page"
    })
    
    count = db.waitlist.count_documents({})
    return jsonify({"message": "Added to waitlist", "count": count}), 201

@app.route('/api/waitlist/count', methods=['GET'])
def waitlist_count():
    count = db.waitlist.count_documents({})
    return jsonify({"count": count})

@app.route('/api/waitlist/emails', methods=['GET'])
def waitlist_emails():
    emails = list(db.waitlist.find({}, {"email": 1, "created_at": 1}).sort("created_at", -1))
    return jsonify([serialize_doc(e) for e in emails])

@app.route('/api/purchase', methods=['POST'])
def purchase_data():
    data = request.get_json()
    plan_id = data.get('plan_id')
    plan_name = data.get('plan_name')
    amount = data.get('amount')

    if not plan_id or not plan_name or amount is None:
        return jsonify({'error': 'Missing plan details'}), 400

    purchase_record = {
        'plan_id': plan_id,
        'plan_name': plan_name,
        'amount': amount,
        'status': 'completed',
        'timestamp': datetime.utcnow().isoformat()
    }

    # Optional: Save to MongoDB if you have a purchases collection
    # db.purchases.insert_one(purchase_record)

    return jsonify({
        'success': True,
        'message': f'Purchased {plan_name} successfully',
        'purchase': purchase_record
    }), 200

if __name__ == '__main__':
    print("🚀 DCN API v2 starting...")
    print(f"📊 SIMs in DB: {db.sims.count_documents({})}")
    print(f"📧 Waitlist entries: {db.waitlist.count_documents({})}")
    app.run(host='0.0.0.0', port=5000, debug=True)