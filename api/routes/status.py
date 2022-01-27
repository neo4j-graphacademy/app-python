from flask import Blueprint, current_app, jsonify

status_routes = Blueprint("status", __name__, url_prefix="/api/status")

@status_routes.route('/', methods=['GET'])
def get_index():
    return jsonify({
        "driver": current_app.driver is not None,
        "NEO4J_URI": current_app.config.get('NEO4J_URI'),
        "NEO4J_USERNAME": current_app.config.get('NEO4J_USERNAME'),
        "NEO4J_PASSWORD": current_app.config.get('NEO4J_PASSWORD'),
        "NEO4J_DATABASE": current_app.config.get('NEO4J_DATABASE'),
        "JWT_SECRET": current_app.config.get('JWT_SECRET'),
    })