from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
import spacy

main_bp = Blueprint('main', __name__)
CORS(main_bp)
nlp = spacy.load("en_core_web_sm")

# Synonym dictionary for demonstration purposes
synonyms = {
    "introduction": ["intro", "beginning", "start"],
    "main topic": ["main subject", "central theme", "core idea"],
    "conclusion": ["end", "summary", "wrap-up"]
}

def is_point_covered(transcript_tokens, point):
    point_text_lower = point.lower()
    if point_text_lower in transcript_tokens:
        return True

    for synonym in synonyms.get(point_text_lower, []):
        if synonym in transcript_tokens:
            return True

    return False

@main_bp.route('/')
def index():
    return render_template('index.html.j2')

@main_bp.route('/live')
def live():
    return render_template('live.html.j2')

@main_bp.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    transcript = data['transcript']
    points = data['points']

    doc = nlp(transcript)
    transcript_tokens = [token.text.lower() for token in doc]
    print(f"Transcript Tokens: {transcript_tokens}")

    for point in points:
        if is_point_covered(transcript_tokens, point['text']):
            point['covered'] = True
            print(f"Point '{point['text']}' covered")
        else:
            print(f"Point '{point['text']}' not covered")

    return jsonify(points)