__author__ = 'mike'


from flask import Flask, url_for, redirect, flash
from project import app, db


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')



@app.route('/', defaults={'page':'index'})
def index(page):
    return redirect(url_for('posts.home'))