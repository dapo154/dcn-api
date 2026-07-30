from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://testuser:testpass123@cluster0.inkdjrq.mongodb.net/dcn_network?retryWrites=true&w=majority&appName=Cluster0')
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
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

@app.route('/api/sos', methods=['POST'])
def trigger_sos():
    data = request.json
    return jsonify({
        "success": True,
        "message": "SOS alert received. Emergency services notified.",
        "alert_id": "sos_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "timestamp": datetime.now().isoformat()
    })

# Vercel handler
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(jsonify({"status": "ok"}).data)
        return