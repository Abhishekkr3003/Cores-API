from flask import Blueprint, jsonify

index = Blueprint('index', __name__)


@index.route("/")
def home():
    response = jsonify("Running");
    response.status_code = 200
    return response
