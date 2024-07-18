from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
#from utils import is_point_covered, process_transcript
import sqlite3


import os
import psycopg2
from jinja2 import Environment, FileSystemLoader

# Database connection parameters
db_params = {
    'dbname': 'neurocator',
    'user': 'neurocator_owner',
    'password': 'cLDe5qNvzUO1',  # In production, use environment variables for sensitive data
    'host': 'ep-dark-forest-a6dtlznj.us-west-2.aws.neon.tech',
    'port': '5432'  # Default PostgreSQL port, change if your setup is different
}
# Connect to the database
conn = psycopg2.connect(**db_params)
# Create a cursor
cur = conn.cursor()
conn.commit()


app = Flask(__name__)
CORS(app)

# # Initialize the SQLite database for the to-do list
# def init_db():
#     with sqlite3.connect('database.db') as conn:
#         c = conn.cursor()
#         c.execute('''CREATE TABLE IF NOT EXISTS tasks
#                      (task TEXT, completed BOOLEAN)''')
#         conn.commit()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('login.html.j2', username=session.get('aanikatangirala_username'))

    
@app.route('/checklogin', methods=['GET', 'POST'])
def checkLogin():
    inputUsername = request.values.get("email")
    inputPassword = request.values.get("password")
    inputs = ['email', 'password']
    validated = serverSideValidation(inputs)
    if validated == True:
        query = "SELECT password FROM users WHERE username=%s"
        queryVars = (inputUsername, )
        cur.execute(query, queryVars)
        conn.commit()
        results = cur.fetchall()
        if (len(results) == 1):
            hashedPassword = results[0]['password']
            if check_password_hash(hashedPassword, inputPassword):
                session['neurocator_username'] = inputUsername
                return redirect(url_for('index'))

        

# general server-side validation 
def serverSideValidation(inputs):
    for input in inputs:
        if (len(request.values.get(input)) == 0):
            validated = False
        else:
            validated = True
    return validated

@app.route('/live', methods=['GET', 'POST'])
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
            if is_point_covered(transcript_tokens, point['text']):
                point['covered'] = True
                print(f"Point '{point['text']}' covered")
            else:
                point['covered'] = False
                print(f"Point '{point['text']}' not covered")

        return jsonify(points)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    return render_template('forum.html.j2')

@app.route('/longtermplanning')
def planning():
    return render_template('longtermplanning.html.j2')

@app.route('/resources')
def resources():
    return render_template('resources.html.j2')

@app.route('/about')
def about():
    return render_template('about_us.html.j2')

# To-Do List routes
@app.route('/todo', methods=['GET', 'POST'])
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
            c.execute('DELETE FROM tasks WHERE rowid = ?', (task_id,))
            conn.commit()
        return redirect(url_for('to_do_list'))
    except Exception as e:
        print(f"Error completing task {task_id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/faq')
def faq():
    return render_template('faq.html.j2')

if __name__ == '__main__':
    #init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)