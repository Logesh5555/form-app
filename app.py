from flask import Flask, render_template, request
import mysql.connector
import os
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def form():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    db = None
    cursor = None

    try:
        # ✅ Check env variables
        if not os.environ.get("DB_HOST"):
            return "❌ Database not configured"

        db = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            port=int(os.environ.get("DB_PORT", 41059)),
            connection_timeout=5
        )

        if db.is_connected():
            print("✅ Database Connected")

        cursor = db.cursor()

        query = "INSERT INTO submissions (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))

        db.commit()

    except Exception as e:
        print("❌ Error:", e)
        return f"Database Error: {e}"

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("success.html", name=name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Server starting on port {port}...")
    serve(app, host="0.0.0.0", port=port)