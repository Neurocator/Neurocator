from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/forum', methods=['GET','POST'])
def forum():
    return render_template('forum.html.j2')

@app.route('/live')
def live():
    return render_template("live.html")

@app.route('/about')
def about():
    return render_template("about_us.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#if __name__ == '__main__':
#    app.run(debug=True)
    
