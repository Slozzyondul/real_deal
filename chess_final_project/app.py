from flask import Flask, render_template, jsonify, request, url_for, redirect, session
#importing modules
from random import shuffle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__== '__main__':
    app.run(debug=True)