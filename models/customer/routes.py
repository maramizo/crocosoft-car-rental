import json

import MySQLdb._exceptions
from flask import Response, request
from app import app
from models.customer.methods import Customer
from misc.errors import error
prefix = '/customer/'


@app.route(prefix + '<int:_id>', methods=['GET'])
def get_customer(_id: int):
    customer = Customer(_id).get()
    return Response(customer.jsonify(), mimetype="application/json") if customer else error('Customer not found.', 404)


@app.route(prefix + '<int:_id>', methods=['POST'])
def update_customer(_id: int):
    return Response(Customer(id=_id, **request.json).save().jsonify(), mimetype="application/json")


@app.route(prefix + '<int:_id>', methods=['DELETE'])
def delete_customer(_id: int):
    Customer(id=_id).delete()
    return Response(json.dumps({"result": "Booking deleted."}), mimetype="application/json")


@app.route(prefix + '/create', methods=['POST'])
def create_customer():
    try:
        return Response(Customer(**request.get_json()).save().jsonify(), mimetype="application/json")
    except MySQLdb._exceptions.IntegrityError:
        return error('Email already exists.')
