import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://zzfyhrcnyiczcp' \
                                        ':d0b65cebf65951da4f256f40e5279e66ad0410dc79c9119c05d25ba542474379@ec2-34-254' \
                                        '-69-72.eu-west-1.compute.amazonaws.com:5432/dd1oun8h39mb7n'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Storage class/Model
class Storage(db.Model):
    __tablename__ = 'storage'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    amount = db.Column(db.Integer)
    measure = db.Column(db.String(10))
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __init__(self, title, amount, measure, price, cost, date):
        self.title = title
        self.amount = amount
        self.measure = measure
        self.price = price
        self.cost = cost
        self.date = date


@app.route('/resources', methods=['POST'])
def input_data():
    post_data = request.get_json()
    title = post_data.get('title')
    amount = post_data.get('amount')
    measure = post_data.get('measure')
    price = post_data.get('price')
    cost = price * amount
    date = datetime.strptime((post_data.get('date')), '%d-%m-%Y')
    comm = Storage(title, amount, measure, price, cost, date)
    db.session.add(comm)
    db.session.commit()
    return jsonify('Data posted')


@app.route('/resources', methods=['GET'])
def get_data():
    resources = Storage.query.all()
    pre_res = []
    for resource in resources:
        result = {'title': resource.title, 'id': resource.id, 'amount': resource.amount, 'measure': resource.measure,
                  'price': resource.price, 'cost': resource.cost, 'date': str(resource.date)}
        pre_res.append(result)
    return jsonify({'resources': pre_res})


@app.route('/resources', methods=['DELETE'])
def del_data():
    id = request.args.get('id')
    resource = db.session.query(Storage).get(id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify('Deleted')


@app.route('/resources', methods=['PUT'])
def update_data():
    id = request.args.get('ID')
    rec = db.session.query(Storage).get(id)
    rec.id = request.args.get('ID')
    rec.amount = request.args.get('amount')
    rec.price = request.args.get('price')
    rec.date = datetime.strptime((request.args.get('date')), '%d-%m-%Y')
    rec.title = request.args.get('title')
    rec.cost = int(rec.price) * int(rec.amount)
    db.session.commit()
    return jsonify('Successfully updated!')


@app.route('/total_cost', methods=['GET'])
def total_cost():
    resources = Storage.query.all()
    total_cost = sum([resource.cost for resource in resources])
    return jsonify({'total_cost': total_cost})


if __name__ == '__main__':
    app.run(debug=False)
