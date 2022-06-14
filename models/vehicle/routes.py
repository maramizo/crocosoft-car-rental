import json

from flask import Response, request
from app import app
from models.vehicle.methods import Vehicle
from misc.errors import error
prefix = '/vehicle/'


@app.route(prefix + '<int:_id>', methods=['GET'])
def get_vehicle(_id: int):
    vehicle = Vehicle(_id).get()
    return Response(vehicle.jsonify(), mimetype="application/json") if vehicle else error('Vehicle not found.', 404)


@app.route(prefix + '<int:_id>', methods=['POST'])
def update_vehicle(_id: int):
    return Response(Vehicle(id=_id, **request.json).save().jsonify(), mimetype="application/json")


@app.route(prefix + '<int:_id>', methods=['DELETE'])
def delete_vehicle(_id: int):
    Vehicle(id=_id).delete()
    return Response(json.dumps({"result": "Vehicle deleted."}), mimetype="application/json")


@app.route(prefix + '/create', methods=['POST'])
def create_vehicle():
    return Response(Vehicle(**request.get_json()).save().jsonify(), mimetype="application/json")
