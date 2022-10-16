from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from fluent import sender
from fluent import event
import json
import random


app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testpwd@postgres:5432/postgres'
logger = sender.FluentSender('app', host='localhost', port=24225)


class Numbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer)


@app.route('/')
def index():
    ret = logger.emit('test', {'path': '/'})
    if not ret:
        print(logger.last_error)
    return json.dumps([float(n.data) for n in Numbers.query.limit(10).all()])


@app.route('/add', methods=['POST'])
def add():
    logger.emit('test', {'path': '/add'})
    Numbers(data=random.random())
    db.session.flush()
    return 'Created', 200


@app.route('/sum')
def all():
    logger.emit('test', {'path': '/sum'})
    return sum([float(n.data) for n in Numbers.query.all()])
