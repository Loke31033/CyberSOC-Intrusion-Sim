from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

@app.route('/')
def index():
    return "CyberSOC Flask API running"

@app.route('/api/iocs')
def get_iocs():
    path = os.path.join(REPORTS_DIR, 'iocs.json')
    if not os.path.exists(path):
        return jsonify({})
    with open(path) as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/findings')
def get_findings():
    path = os.path.join(REPORTS_DIR, 'findings.txt')
    if not os.path.exists(path):
        return jsonify([])
    with open(path) as f:
        findings = f.read().splitlines()
    return jsonify(findings)

@app.route('/api/timeline')
def get_timeline():
    path = os.path.join(REPORTS_DIR, 'timeline.csv')
    if not os.path.exists(path):
        return jsonify([])
    timeline = []
    with open(path) as f:
        next(f)  # skip header
        for line in f:
            timestamp, desc = line.strip().split(",", 1)
            timeline.append({"timestamp": timestamp, "description": desc})
    return jsonify(timeline)

if __name__ == '__main__':
    app.run(debug=True)

