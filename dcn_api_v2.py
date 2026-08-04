from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import requests

app = Flask(__name__)
CORS(app)

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://testuser:testpass123@cluster0.inkdjrq.mongodb.net/dcn_network?retryWrites=true&w=majority&appName=Cluster0')
client = MongoClient(MONGODB_URI)
db = client.dcn_network

# Termii Config
TERMII_API_KEY = os.getenv('TERMII_API_KEY', 'tlv_hXPsx6BF8A9f0IbvYqhzYYmlnrxmfzmw1OggyCIqhZI')
TERMII_SENDER_ID = os.getenv('TERMII_SENDER_ID', 'Termii')

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

def send_sms(to, message):
    # Format number for Termii (remove leading 0, add 234)
    formatted = to
    if formatted.startswith('0'):
        formatted = '234' + formatted[1:]
    elif formatted.startswith('+'):
        formatted = formatted[1:]
    
    url = "https://api.ng.termii.com/api/sms/send"
    payload = {
        "to": formatted,
        "from": TERMII_SENDER_ID,
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": TERMII_API_KEY,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"SMS failed: {e}")
        return {"error": str(e)}

@app.route('/')
def home():
    return jsonify({
        "message": "DCN Network API",
        "version": "2.1.0",
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
    phone_number = data.get('phone_number')

    if not plan_id or not plan_name or amount is None:
        return jsonify({'error': 'Missing plan details'}), 400
    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    purchase_record = {
        'plan_id': plan_id,
        'plan_name': plan_name,
        'amount': amount,
        'phone_number': phone_number,
        'status': 'completed',
        'timestamp': datetime.utcnow().isoformat()
    }

    db.purchases.insert_one(purchase_record)

    # Send SMS receipt
    sms_message = f"DCN: You purchased {plan_name} ({plan_id}) for N{amount}. Data will be loaded to {phone_number} shortly. Thank you!"
    sms_result = send_sms(phone_number, sms_message)

    return jsonify({
        'success': True,
        'message': f'Purchased {plan_name} for {phone_number}',
        'purchase': serialize_doc(purchase_record),
        'sms_status': sms_result
    }), 200

@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    purchases = list(db.purchases.find().sort("timestamp", -1).limit(50))
    return jsonify([serialize_doc(p) for p in purchases])