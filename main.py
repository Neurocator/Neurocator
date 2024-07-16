from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/forum')
def forum():
    return render_template("forum.html")

@app.route('/live')
def live():
    return render_template("live_assistance.html")

@app.route('/about')
def about():
    return render_template("about_us.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)