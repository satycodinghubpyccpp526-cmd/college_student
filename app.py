from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS tips(id INTEGER PRIMARY KEY AUTOINCREMENT,
              senior_name TEXT,
              college TEXT,
              branch TEXT,
              title TEXT,
              description TEXT,
              urgency TEXT,
              credibility INTEGER DEFAULT 0,
              create_at TEXT)''')
    conn.commit()
    conn.close()
    
init_db()
@app.route("/")
def home():

    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()

    c.execute("SELECT * FROM tips ORDER BY id DESC")

    tips = c.fetchall()

    conn.close()

    return render_template("index.html", tips=tips)
@app.route("/add_tip",methods = ["POST"])
def add_tip():
    data = request.json
    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()
    c.execute('''INSERT INTO tips(senior_name, college, branch,title,description,urgency, created_at) VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
              (data["senior_name"],
               data["college"],
               data["branch"],
               data["title"],
               data["description"],
               data["urgency"],
               datetime.now().strftime("%Y-%m-%d %H: %M: %S")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Tip added successfully"})
@app.route("/tips", methods = ["GET"])
def get_tips():
    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM tips")
    rows = c.fetchall()
    conn.close()
    tips = []
    
    for row in rows:
        tips.append({
            "id": row[0],
            "senior_name": row[1],
            "college": row[2],
            "branch": row[3],
            "title": row[4],
            "description": row[5],
            "urgency": row[6],
            "credibility": row[7],
            "created_at": row[8]
        })
    return jsonify(tips)

if __name__ == "__main__":
    app.run(debug = True)
