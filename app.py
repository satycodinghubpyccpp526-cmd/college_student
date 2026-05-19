from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3
from datetime import datetime
app = Flask(__name__)
app.secret_key="college_secret"

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
              created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password TEXT)''')
    conn.commit()
    conn.close()
    
init_db()

@app.route("/")
def home():
    
    college = request.args.get("college")
    branch = request.args.get("branch")
    urgency = request.args.get("urgency")
    
    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()
    query = "SELECT * FROM tips WHERE 1=1"
    params = []
    
    if college:
        query += " AND college=?"
        params.append(college)
        
    if branch:
        query += " AND branch=?"
        params.append(branch)
        
    if urgency:
        query += " AND urgency=?"
        params.append(urgency)

    c.execute(query, params)

    tips = c.fetchall()

    conn.close()

    return render_template("index.html", tips=tips)

@app.route("/add_tip", methods=["POST"])
def add_tip():

    senior_name = request.form["senior_name"]
    college = request.form["college"]
    branch = request.form["branch"]
    title = request.form["title"]
    description = request.form["description"]
    urgency = request.form["urgency"]

    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO tips
    (senior_name, college, branch, title, description, urgency, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        senior_name,
        college,
        branch,
        title,
        description,
        urgency,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/verify/<int:id>")
def verify(id):
    conn = sqlite3.connect("college_intel.db")
    c = conn.cursor()
    c.execute("UPDATE tips SET credibility = credibility + 1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
    return redirect("/")

@app.route("/signup",methods = ["GET","POST"])
def signup():
    if request.method=="POST":
        
        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("college_itel.db")
        c=conn.cursor()
        c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("signup.html")

@app.route("/login")
def login():
    if request.method == "POST":
        username = request.form["username"]
        username = request.form["password"]
        conn = sqlite3.connect("college_intel.db")
        c = conn.cursor()
        
        c.execute(
            "SELECT * FROM user WHERE username=? AND password=?",(username, password)
        )
        user = c.fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid Username or Password"
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
        
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
