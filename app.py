from flask import Flask, render_template, request
from abusetofunny import abusetofunny

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def hate_to_funny():
    if request.method == 'POST':
        hate = request.form['hateText']
        funny = abusetofunny(hate)
        return render_template('index.html', hateMessage = hate, funnyMessage = funny)
    return render_template('index.html', hateMessage = '', funnyMessage = '')

if __name__ == '__main__':
    app.run(debug = False)
