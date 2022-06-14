import json
from datetime import timedelta
from flask import Response, request
from app import app
from models.booking.methods import Booking
from misc.errors import error
prefix = '/booking/'


@app.route(prefix + '<int:_id>', methods=['GET'])
def get_booking(_id: int):
    booking = Booking(_id).get()
    return Response(booking.jsonify(), mimetype="application/json") if booking else error('Booking not found.', 404)


@app.route(prefix + '<int:_id>', methods=['POST'])
def update_booking(_id: int):
    return Response(Booking(id=_id, **request.json).save().jsonify(), mimetype="application/json")


@app.route(prefix + '<int:_id>', methods=['DELETE'])
def delete_booking(_id: int):
    Booking(id=_id).delete()
    return Response(json.dumps({"result": "Booking deleted."}), mimetype="application/json")


@app.route(prefix + '/create', methods=['POST'])
def create_booking():
    booking = Booking(**request.get_json())
    if booking.hire_date > booking.end_date:
        return error('Hire date must be before end date.', 400)
    if booking.end_date - booking.hire_date > timedelta(days=7):
        return error('Booking must be less than or equal to 7 days.', 400)
    booking = booking.save()
    return Response(booking.jsonify(), mimetype="application/json")
