__author__ = 'Mike Norman'

from flask import Flask, flash, redirect, url_for, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
#from forms import CreateTaskForm


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task


@app.route('/hello_world')
def hello_world():
    return 'Hello World'

@app.route('/')
def index():

    open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.task_id.asc())
    return render_template("index.html", open_tasks=open_tasks)


@app.route('/addTask/', methods=["POST"])
def add_task():
    task = request.form['task']
    if not task:
        error = "You suck"
        flash("you have to enter a task")
        return redirect(url_for('index'))
    else:
        db.session.add(Task(request.form['task'], 1))
        db.session.commit()
        return redirect(url_for('index'))
