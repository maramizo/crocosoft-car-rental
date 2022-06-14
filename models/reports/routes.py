import json
from datetime import datetime

from flask import Response
from app import app
from models.booking.methods import Booking
from models.vehicle.methods import Vehicle

prefix = '/reports/'


@app.route(prefix + 'today', methods=['GET'])
def booked_today():
    return Response(
        json.dumps({"reports": [x.dict() for x in Booking.get_created_today()]}, default=str),
        mimetype="application/json"
    )


@app.route(prefix + '/vehicles/available/<date:date>', methods=['GET'])
def available_vehicles(date: datetime):
    return Response(
        json.dumps({"vehicles": [x.dict() for x in Vehicle().get_available(date)]}, default=str),
        mimetype="application/json"
    )
