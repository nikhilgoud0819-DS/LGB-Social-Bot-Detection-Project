from flask import Flask, render_template, request, redirect ,session
import sqlite3
import webbrowser
import joblib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "lgb_project_secret"
# Load ML Model
model = joblib.load("model/bot_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Create Database
def init_db():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Users Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    ''')

    # Predictions Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet TEXT,
            prediction TEXT,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Total Tweets
    cur.execute("SELECT COUNT(*) FROM predictions")
    total_tweets = cur.fetchone()[0]

    # Total Bots
    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='Bot'"
    )
    bots = cur.fetchone()[0]

    # Total Humans
    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='Human'"
    )
    humans = cur.fetchone()[0]

    # Latest Prediction
    cur.execute("""
        SELECT prediction
        FROM predictions
        ORDER BY id DESC
        LIMIT 1
    """)
    latest = cur.fetchone()

    if latest:
        latest_result = latest[0]
    else:
        latest_result = "No Data"

    # Recent 5 Predictions
    cur.execute("""
        SELECT tweet, prediction
        FROM predictions
        ORDER BY id DESC
        LIMIT 5
    """)
    recent_predictions = cur.fetchall()

    conn.close()

    accuracy = 95

    if total_tweets > 0:
        bot_percentage = round((bots / total_tweets) * 100, 2)
        human_percentage = round((humans / total_tweets) * 100, 2)
    else:
        bot_percentage = 0
        human_percentage = 0

    return render_template(
        'home.html',
        total_tweets=total_tweets,
        accuracy=accuracy,
        latest_result=latest_result,
        bot_percentage=bot_percentage,
        human_percentage=human_percentage,
        recent_predictions=recent_predictions
    )# Register Page
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username,email,password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
           session['username'] = user[1]
           return redirect('/dashboard')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():

    prediction = None
    confidence = None

    if request.method == 'POST':

        tweet = request.form['tweet']

        # ML Prediction
        tweet_vector = vectorizer.transform([tweet])

        result = model.predict(tweet_vector)
        probability = model.predict_proba(tweet_vector)
        confidence = round(max(probability[0]) * 100, 2)

        if result[0] == 1:
            prediction = "Bot"
        else:
            prediction = "Human"

        # Save Prediction with Date
        current_time = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO predictions
            (tweet, prediction, created_at)
            VALUES (?, ?, ?)
            """,
            (tweet, prediction, current_time)
        )

        conn.commit()
        conn.close()

    # Statistics Section
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM predictions")
    total = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='Bot'"
    )
    bots = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='Human'"
    )
    humans = cur.fetchone()[0]

    conn.close()

    username = session.get('username', 'User')

    return render_template(
        'dashboard.html',
        prediction=prediction,
        confidence=confidence if prediction else None,
        total=total,
        bots=bots,
        humans=humans,
        username=username
    )
@app.route('/history')
def history():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT id, tweet, prediction FROM predictions ORDER BY id DESC"
    )

    records = cur.fetchall()

    conn.close()

    return render_template(
        'history.html',
        records=records
    )
@app.route('/analytics')
def analytics():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM predictions")
    total = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='Bot'"
    )
    bots = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction='Human'"
    )
    humans = cur.fetchone()[0]

    conn.close()

    bot_rate = 0
    human_rate = 0

    if total > 0:
     bot_rate = round((bots / total) * 100, 2)
     human_rate = round((humans / total) * 100, 2)

    return render_template(
    'analytics.html',
    total=total,
    bots=bots,
    humans=humans,
    bot_rate=bot_rate,
    human_rate=human_rate
)


# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Run Application
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)