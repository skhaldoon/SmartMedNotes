from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = '1122'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '051179'
app.config['MYSQL_DB'] = 'smartmednotes'  # Updated database name
mysql = MySQL(app)

# Helper function to validate password
def validate_password(password):
    if len(password) < 4:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()_+" for char in password):
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

# Route for SignUp
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("check1")
    if request.method == 'POST':
        print("check2")
        try:
            print("check3")
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            role = request.form['role']
            date_registered = datetime.now()
            print("check4")
            # Validation checks
            if password != confirm_password:
                print("checka")
                flash("Passwords do not match!")
                print("checkb")
                return redirect(url_for('signup'))

            if len(password) < 4 or not any(c.isdigit() for c in password):
                print("checkd")
                flash("Password must have at least 4 characters, 1 special character, and 1 number!")
                print("checkc")
                return redirect(url_for('signup'))
            print("check5")
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                print("chexk")
                flash("Email already in use!")
                return redirect(url_for('signup'))
            print("check6")
           
            cursor.execute(
                "INSERT INTO users(username, email, password, role, date_registered) VALUES(%s, %s, %s, %s, %s)",
                (username, email, password, role, date_registered)
            )
            print("check8")
            mysql.connection.commit()
            flash("Registration successful!")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error: {e}")
            return redirect(url_for('signup'))
        finally:
            print("check9")
            if 'cursor' in locals():
                cursor.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and user[3] == password:  # Assuming password is at index 3
                flash("Login successful!")
                return redirect(url_for('index'))
            else:
                flash("Invalid credentials!")
                return redirect(url_for('login'))

        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('login'))

        finally:
            cursor.close()

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
