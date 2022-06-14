import json

from flask import Response, request
from app import app
from models.category.methods import Category
from misc.errors import error
prefix = '/category/'


@app.route(prefix + '<int:_id>', methods=['GET'])
def get_category(_id: int):
    category = Category(_id).get()
    return Response(category.jsonify(), mimetype="application/json") if category else error('Category not found.', 404)


@app.route(prefix + '<int:_id>', methods=['POST'])
def update_category(_id: int):
    return Response(Category(id=_id, **request.json).save().jsonify(), mimetype="application/json")


@app.route(prefix + '<int:_id>', methods=['DELETE'])
def delete_category(_id: int):
    Category(id=_id).delete()
    return Response(json.dumps({"result": "Category deleted."}), mimetype="application/json")


@app.route(prefix + '/create', methods=['POST'])
def create_category():
    return Response(Category(**request.get_json()).save().jsonify(), mimetype="application/json")
