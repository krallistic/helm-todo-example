import os

from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    os.environ['MONGO_DB_ADDRESS'],
    os.environ['MONGO_DB_PORT'])
db = client.tododb


@app.route('/')
def todo():
    todos = [todo for todo in db.tododb.find()]

    return render_template('todo.html', items=todos)


@app.route('/healthz')
def healthz():
    return "OK"

@app.route('/readyz')
def readyz():
    return "OK"

@app.route('/new', methods=['POST'])
def new():

    todo_doc = {
        'title': request.form['title'],
        'description': request.form['description'],
        'date': request.form['date']
    }
    db.tododb.insert_one(todo_doc)

    return redirect(url_for('todo'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)