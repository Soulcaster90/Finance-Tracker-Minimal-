from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DB_PATH = "expenses.db"

# Initialize database if not exists
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(open("schema.sql").read())
        conn.commit()
        conn.close()

init_db()

# Add expense
@app.route("/add", methods=["POST"])
def add_expense():
    data = request.json
    desc = data.get("description")
    cat = data.get("category")
    amount = data.get("amount")
    date = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (description, category, amount, date) VALUES (?, ?, ?, ?)",
              (desc, cat, amount, date))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# Get all expenses
@app.route("/expenses")
def get_expenses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, description, category, amount, date FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    result = [{"id": r[0], "description": r[1], "category": r[2], "amount": r[3], "date": r[4]} for r in rows]
    return jsonify(result)

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)