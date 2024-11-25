from . import auth
from flask import jsonify

@auth.route('/')
def index():
    return jsonify({"message": "hello world"})