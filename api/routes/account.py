from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import current_user, jwt_required

from api.dao.favorites import FavoriteDAO
from api.dao.ratings import RatingDAO

account_routes = Blueprint("account", __name__, url_prefix="/api/account")

@account_routes.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    return jsonify(current_user)

@account_routes.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    # Get user ID from JWT
    user_id = current_user["sub"]

    # Get search parameters
    sort = request.args.get("sort", "title")
    order = request.args.get("order", "ASC")
    limit = request.args.get("limit", 6, type=int)
    skip = request.args.get("skip", 0, type=int)

    # Create the DAO
    dao = FavoriteDAO(current_app.driver)

    output = dao.all(user_id, sort, order, limit, skip)

    return jsonify(output)

@account_routes.route('/favorites/<movie_id>', methods=['POST', 'DELETE'])
@jwt_required()
def add_favorite(movie_id):
    # Get user ID from JWT
    user_id = current_user["sub"]

    # Create the DAO
    dao = FavoriteDAO(current_app.driver)

    if request.method == "POST":
        # Save the favorite
        output = dao.add(user_id, movie_id)
    else:
        # Remove the favorite
        output = dao.remove(user_id, movie_id)

    # Return the output
    return jsonify(output)


@account_routes.route('/ratings/<movie_id>', methods=['POST'])
@jwt_required()
def save_rating(movie_id):
    # Get user ID from JWT
    user_id = current_user["sub"]

    # Get rating from Request
    form_data = request.get_json()
    rating = int(form_data["rating"])

    # Create the DAO
    dao = RatingDAO(current_app.driver)

    # Save the rating
    output = dao.add(user_id, movie_id, rating)

    # Return the output
    return jsonify(output)

