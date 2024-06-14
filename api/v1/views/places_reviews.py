#!/usr/bin/python3
"""
Review object that handles all default RESTFul API actions
"""
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
@swag_from('documentation/review/get_reviews.yml', methods=['GET'])
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/review/get_review.yml', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/review/delete_review.yml', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
@swag_from('documentation/review/post_review.yml', methods=['POST'])
def post_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    user_id = data.get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    data["place_id"] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/review/put_review.yml', methods=['PUT'])
def put_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
