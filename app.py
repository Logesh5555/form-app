from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def form():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="logi",
            database="form_db"
        )

        cursor = db.cursor()

        query = "INSERT INTO submissions (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))

        db.commit()

    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        db.close()

    return render_template("success.html", name=name)

if __name__ == '__main__':
    app.run(debug=True)