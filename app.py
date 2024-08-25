import os
import psycopg2
import logging
import sqlite3
from functools import wraps
from flask import Flask, request, render_template, jsonify, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
from datetime import date
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Database connection parameters
db_params = {
    'dbname': os.getenv('PGDATABASE', 'neurocator'),
    'user': os.getenv('PGUSER', 'neurocator_owner'),
    'password': os.getenv('PGPASSWORD', '3j1HgiIuwVoO'),
    'host': os.getenv('PGHOST', 'ep-autumn-scene-a6huvqfz.us-west-2.aws.neon.tech'),
    'port': os.getenv('PGPORT', '5432'),
    'sslmode': 'require'
}
conn = psycopg2.connect(**db_params)
cur = conn.cursor()
# Utility functions
def is_point_covered(transcript_tokens, point_text):
    return point_text.lower() in transcript_tokens
def process_transcript(transcript):
    return transcript.split()
# Initialize Flask app
app = Flask(__name__)
CORS(app)
session_username_key = 'neurocator_username'
app.config['SECRET_KEY'] = "bflerjvnlkrv#123"
# Ensure SQLite tasks table exists
def init_sqlite_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
init_sqlite_db()
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('home.html.j2')
@app.route('/login', methods=['GET'])
def login():
    print(session.get(session_username_key))
    if request.method == 'GET':
        return render_template('login.html.j2', username=session.get(session_username_key))
@app.route('/logout', methods=['GET'])
def logout():
    print(session.get(session_username_key))
    session.__setitem__(session_username_key, None)
    print(session.get(session_username_key))
    if request.method == 'GET':
        return render_template('home.html.j2', username=None)
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        return render_template('signup.html.j2')
    else:
        inputEmail = request.values.get("email")
        inputUsername = request.values.get("username")
        userTypedPassword = request.values.get("password")
        securedPassword = generate_password_hash(userTypedPassword)
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        query = "SELECT username FROM users WHERE username=%s"
        cur.execute(query, (inputUsername,))
        conn.commit()
        results = cur.fetchall()
        if len(results) == 1:
            return redirect(url_for('signUp', usernameTaken=True))
        else:
            query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
            cur.execute(query, (inputEmail, inputUsername, securedPassword))
            conn.commit()
            return redirect(url_for('login'))
@app.route('/checklogin', methods=['POST'])
def checkLogin():
    inputUsername = request.values.get("username")
    inputPassword = request.values.get("password")
    query = "SELECT password FROM users WHERE username=%s"
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute(query, (inputUsername,))
    conn.commit()
    results = cur.fetchall()
    if len(results) == 1:
        hashedPassword = results[0][0]
        if check_password_hash(hashedPassword, inputPassword):
            session[session_username_key] = inputUsername
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login', incorrectLoginError=True))
    else:
        return redirect(url_for('login', incorrectLoginError=True))
def check_user_loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session.get(session_username_key))
        if session.get(session_username_key) is None:
            # Redirect to login page if not logged in
            return redirect(url_for('login'))
        return f(*args, **kwargs)  # Continue to the requested page if logged in
    return decorated_function
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html.j2')
@app.route('/forum', methods=['GET', 'POST'])
@check_user_loggedin
def forum():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    query = "SELECT id, username, title, content, date FROM posts"
    cur.execute(query)
    conn.commit()
    rows = cur.fetchall()
    posts = []
    print(rows)
    for row in reversed(rows):
        post = {
            'id': row[0],
            'username': row[1],
            'title': row[2],
            'content': row[3],
            'date': row[4]
        }
        posts.append(post)
    return render_template('forum.html.j2', posts=posts)
@app.route('/addpost', methods=['GET', 'POST'])
@check_user_loggedin
def addPost():
    if request.method == 'GET':
        username = session.get(session_username_key)
        return render_template('addpost.html.j2', username=username)
    else:
        username = session.get(session_username_key)
        inputTitle = request.values.get("title")
        inputContent = request.values.get("content")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")  # format the date as YYYY-MM-DD
        query = "INSERT INTO posts (username, title, content, date) VALUES (%s, %s, %s, %s)"
        queryVars = (username, inputTitle, inputContent, (date_str,))
        cur.execute(query, queryVars)
        conn.commit()
        conn.commit()
        return redirect(url_for('forum'))
@app.route('/live', methods=['GET', 'POST'])
@check_user_loggedin
def live():
    if request.method == 'POST':
        points = request.form.getlist('points')
        points = [{"text": point, "covered": False} for point in points]
        return render_template('live.html.j2', points=points)
    return render_template('live.html.j2', points=[])
@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        data = request.get_json()
        transcript = data.get('transcript', '')
        points = data.get('points', [])
        if not transcript or not points:
            return jsonify({"error": "Invalid input data"}), 400
        transcript_tokens = process_transcript(transcript)
        print(f"Transcript Tokens: {transcript_tokens}")
        for point in points:
            if not point['covered'] and is_point_covered(transcript_tokens, point['text']):
                point['covered'] = True
                print(f"Point '{point['text']}' covered")
            for subpoint in point.get('subpoints', []):
                if not subpoint['covered'] and is_point_covered(transcript_tokens, subpoint['text']):
                    subpoint['covered'] = True
                    print(f"Subpoint '{subpoint['text']}' covered")
        return jsonify(points)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/longtermplanning')
def planning():
    return render_template('longtermplanning.html.j2')
@app.route('/resources')
def resources():
    return render_template('resources.html.j2')
@app.route('/about')
def about():
    return render_template('about_us.html.j2')
@app.route('/todo', methods=['GET', 'POST'])
@check_user_loggedin
def to_do_list():
    if request.method == 'POST':
        task = request.form['task']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO tasks (task, completed) VALUES (?, ?)', (task, False))
            conn.commit()
        return redirect(url_for('to_do_list'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT rowid, task, completed FROM tasks')
        tasks = [(rowid, task, completed) for rowid, task, completed in c.fetchall()]
    print(f"Tasks: {tasks}")  # Debug output
    return render_template('to_do_list.html.j2', tasks=tasks)
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE tasks SET completed = NOT completed WHERE rowid = ?', (task_id,))
            conn.commit()
        return redirect(url_for('to_do_list'))
    except Exception as e:
        print(f"Error completing task {task_id}: {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tasks WHERE rowid = ?', (task_id,))
            conn.commit()
        return redirect(url_for('to_do_list'))
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/faq')
def faq():
    return render_template('faq.html.j2')
@app.route('/download/<path:filename>')
def download(filename):
    directory = os.path.join(app.root_path, 'static/files/article')
    return send_from_directory(directory, filename)
# general server-side validation
def serverSideValidation(inputs):
    for input in inputs:
        if len(request.values.get(input)) == 0:
            validated = False
        else:
            validated = True
    return validated
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)