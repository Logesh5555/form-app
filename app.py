from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ✅ HOME PAGE (FORM PAGE)
@app.route('/')
def home():
    return render_template("form.html")


# ✅ SUCCESS PAGE (GET ONLY)
@app.route('/success')
def success():
    name = request.args.get('name')
    return render_template("success.html", name=name)


# ✅ SUBMIT (POST ONLY)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    db = None
    cursor = None

    try:
        db = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            port=int(os.environ.get("DB_PORT")),
            connection_timeout=5
        )

        cursor = db.cursor()

        query = "INSERT INTO submissions (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))

        db.commit()

    except Exception as e:
        return f"Database Error: {e}"

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    # ✅ IMPORTANT: REDIRECT AFTER POST
    return redirect(url_for('success', name=name))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Server running on port {port}")
    serve(app, host="0.0.0.0", port=port)