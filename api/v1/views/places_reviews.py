#!/usr/bin/python3
'''
view for Review object that handles all default RESTFul API actions
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models import storage


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):
    '''Retrieves the list of all Review objects of a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort (404)
    reviews = [reviews.to_dict for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    '''Retrieves review by id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                strict_slashes=False)
def delete_review(review_id):
    '''Delete review of specified id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/place/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Creates a new place review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')
    review_info = request.get_json()

    user_id = review_info['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'text' not in review_info.keys():
        abort(400, 'Missing text')

    new_revw = Review(**review_info)
    new_revw.place_id = place_id
    new_revw.user_id = user_id
    storage.new(new_revw)
    storage.save()

    return jsonify(review.to_dict()), 201
