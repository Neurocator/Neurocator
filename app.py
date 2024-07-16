from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/forum', methods=['GET','POST'])
def forum():
    return render_template('forum.html.j2')

#if __name__ == '__main__':
#    app.run(debug=True)
    
