import json
from flask import Response


def error(_str: str, code: int = 400):
    return Response(json.dumps({"error": _str}), code, mimetype='application/json')
