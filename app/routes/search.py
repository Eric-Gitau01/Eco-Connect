from flask import Blueprint, jsonify

search_bp = Blueprint('search', __name__, url_prefix='/api/search')

@search_bp.route('/', methods=['GET'])
def search():
    return jsonify("Search endpoint is working!")
