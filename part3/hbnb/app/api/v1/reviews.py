from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Input model for POST/PUT
review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Output model for GET
review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_input_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new review.

        Validates the input and registers a new review linked to a user and a place.
        """
        current_user = get_jwt_identity()
        review_data = api.payload

        place_id = review_data.get('place_id')
        if not place_id:
            return {'error': 'place_id is required'}, 400

        # Vérifie que le lieu existe
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Interdit de reviewer son propre lieu
        if place.owner.id == current_user['id']:
            return {'error': 'You cannot review your own place.'}, 400

        # Vérifie si l'utilisateur a déjà review ce lieu
        existing_reviews = facade.get_reviews_by_place(place_id)
        for review in existing_reviews:
            if review.user.id == current_user['id']:
                return {'error': 'You have already reviewed this place.'}, 400

        # Remplace user_id par celui authentifié (évite la triche)
        review_data['user_id'] = current_user['id']

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user.id,
            'place_id': new_review.place.id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve all reviews.

        Returns:
            A list of all reviews with their associated user and place IDs.
        """
        reviews = facade.get_all_reviews()
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id,
                'place_id': r.place.id
            } for r in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Retrieve a specific review by ID.
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_input_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """
        Update an existing review.

        Only the `text` and `rating` fields can be updated.
        """
        current_user = get_jwt_identity()
        review_data = api.payload

        # Vérifie que la review existe
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # User n'a pas crée la review
        if review.user.id != current_user['id']:
            return {'error': 'Unauthorized action.'}, 403

        try:
            updated_review = facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review by ID.
        """
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve all reviews associated with a specific place.

        Args:
            place_id (str): ID of the place whose reviews are requested.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id,
                'place_id': r.place.id
            } for r in reviews
        ], 200
