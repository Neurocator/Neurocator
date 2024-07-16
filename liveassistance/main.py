from flask import Flask, request, jsonify, render_template_string
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
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lecture Tracker</title>
        <style>
            .bullet-point {
                display: flex;
                justify-content: space-between;
                margin-bottom: 5px;
            }
            .crossed-off {
                text-decoration: line-through;
            }
        </style>
    </head>
    <body>
        <h1>Lecture Tracker</h1>
        <div id="bulletPoints">
            <div class="bullet-point" id="point0">Introduction</div>
            <div class="bullet-point" id="point1">Main Topic</div>
            <div class="bullet-point" id="point2">Conclusion</div>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                const points = [
                    {text: "Introduction", covered: false},
                    {text: "Main Topic", covered: false},
                    {text: "Conclusion", covered: false}
                ];

                const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.lang = 'en-US';
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript.toLowerCase();
                    console.log('Transcript:', transcript);
                    fetch('/transcribe', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ transcript, points })
                    })
                    .then(response => response.json())
                    .then(data => {
                        data.forEach((point, index) => {
                            if (point.covered) {
                                document.getElementById(`point${index}`).classList.add('crossed-off');
                            }
                        });
                    });
                };

                recognition.start();

                recognition.onend = () => {
                    recognition.start();
                };
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

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