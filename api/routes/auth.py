from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import current_user

from api.dao.auth import AuthDAO

auth_routes = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_routes.route('/register', methods=['POST'])
def register():
    form_data = request.get_json()

    email = form_data['email']
    password = form_data['password']
    name = form_data['name']

    dao = AuthDAO(current_app.driver, current_app.config.get('SECRET_KEY'))

    user = dao.register(email, password, name)

    return user


@auth_routes.route('/login', methods=['POST'])
def login():
    form_data = request.get_json()

    email = form_data['email']
    password = form_data['password']

    dao = AuthDAO(current_app.driver, current_app.config.get('SECRET_KEY'))

    user = dao.authenticate(email, password)

    if user is False:
        return "Unauthorized", 401

    return jsonify(user)
