from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app) 

DB_FILE = "metrics.db"

def init_db():
    """Skapar databastabellen om den inte finns"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT NOT NULL,
                cpu_usage REAL,
                ram_usage REAL,
                disk_usage REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Tar emot data från Agenten"""
    data = request.json
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_metrics (hostname, cpu_usage, ram_usage, disk_usage)
                VALUES (?, ?, ?, ?)
            ''', (data['hostname'], data['cpu_usage'], data['ram_usage'], data['disk_usage']))
            conn.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Skickar data till Frontend (Hämtar de senaste 20 raderna)"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row # Gör att vi får svaren som dictionary
        cursor = conn.cursor()
        #Hämtar de 20 senaste mätningarna, sorterat på tid
        cursor.execute('SELECT * FROM system_metrics ORDER BY created_at DESC LIMIT 20')
        rows = cursor.fetchall()
        
        #konvertera till lista och vänd håll
        data = [dict(row) for row in rows]
        return jsonify(data[::-1])

if __name__ == '__main__':
    init_db() 
    print("Running server on port 5001...")
    app.run(port=5001, debug=True)