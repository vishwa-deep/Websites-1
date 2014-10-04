__author__ = 'Mike Norman'

from flask import Flask, flash, redirect, url_for, request, render_template, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
#from forms import CreateTaskForm


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task


#@app.route('/hello_world')
#def hello_world():
#    return 'Hello World'

@app.route('/')
def index():
    open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.task_id.asc())
    return render_template("index.html", open_tasks=open_tasks)


@app.route('/addTask/', methods=["GET", "POST"])
def add_task():

    if request.method == "POST":
        json_results = []
        task = request.form.get('task')
        if not task:
            flash("You have to enter a task")
            return redirect(url_for('index'))
        else:
            db.session.add(Task(task, 1))
            db.session.commit()
            open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.task_id.asc())
            for item in open_tasks:
                data = {
                    'task_status': item.status,
                    'task_id': item.task_id,
                    'task': item.task
                }
                json_results.append(data)
            return jsonify(tasks=json_results)
           # return redirect(url_for('index'))



#@app.route('/addTask/', methods=["POST"])
#def add_task():
#    task = request.form['task']
#    if not task:
#        flash("You have to enter a task")

#        return redirect(url_for('index'))
#    else:
#        db.session.add(Task(task, 1))
#        db.session.commit()
#        return redirect(url_for('index'))





@app.route('/delete_task/<int:task_id>/')
def delete_task(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    #flash("Task was deleted!")
    return redirect(url_for('index'))


@app.route('/update_task/<int:task_id>/', methods=["POST"])
def update_task(task_id):
    new_id = task_id
    val = request.form[str(new_id)]
    db.session.query(Task).filter_by(task_id=new_id).update({'task': val})
    db.session.commit()
    #flash('Task was updated')
    return redirect(url_for('index'))

