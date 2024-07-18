from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import psycopg2
from jinja2 import Environment, FileSystemLoader

# Utility functions
def is_point_covered(transcript_tokens, point_text):
    return point_text.lower() in transcript_tokens

def process_transcript(transcript):
    return transcript.split()

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

# Example query (optional, remove if not needed)
cur.execute("INSERT INTO neurocator (name) VALUES ('hi')") 
conn.commit()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('login.html.j2')

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

@app.route('/download/<path:filename>')
def download(filename):
    directory = os.path.join(app.root_path, 'static/files/article')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)