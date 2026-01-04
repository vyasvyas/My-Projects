from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load trained model
with open('crop_model.pkl', 'rb') as f:
    model = pickle.load(f)
# ------------------- SIGNUP -------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Email already exists", "warning")
        else:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            flash("Signup successful! Please login.", "success")
            return redirect('/login')

        cursor.close()
        conn.close()

    return render_template('signup.html')

# ------------------- LOGIN -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            flash("Login successful", "success")
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")

        cursor.close()
        conn.close()

    return render_template('login.html')

# ------------------- LOGOUT -------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect('/login')


# ---------------- HOME (INDEX) ----------------
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/login')

# ---------------- PREDICT CROP ----------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        flash("Please log in to predict.", "warning")
        return redirect('/login')

    try:
        # Get input values from form
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Create array for prediction
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(input_data)[0]

        # 🔹 Clean English crop name (remove Gujarati)
        clean_name = prediction.split("(")[0].strip().lower()

        # 🔹 Convert to image filename
        image_name = clean_name.replace(" ", "_") + ".jpg"

        # Send result to page
        return render_template('result.html', crop=prediction, image_name=image_name)

    except Exception as e:
        flash(f"Prediction Error: {str(e)}", "danger")
        return redirect('/')

    # ---------------- SHOW USERS (Admin/Test Purpose) ----------------
from database import get_connection

@app.route('/users')
def show_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return str(data)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
