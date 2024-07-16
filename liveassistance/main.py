from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)
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

@app.route('/')
def index():
		return send_from_directory('', 'index.html')

@app.route('/transcribe', methods=['POST'])
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

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8080)