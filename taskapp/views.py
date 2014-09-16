__author__ = 'Mike Norman'

from flask import Flask, flash, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return 'Hello World'

@app.route('/')
def index():
    return render_template("index.html")