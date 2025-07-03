from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from flask import request

api = Namespace('admin', description='Admin operations')

# --- MODELS POUR Swagger UI ---

user_admin_model = api.model('User_Admin', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(description='Whether the user is an admin')
})

user_update_admin_model = api.model('UserUpdate_Admin', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email'),
    'password': fields.String(description='Password'),
    'is_admin': fields.Boolean(description='Admin status')
})

amenity_admin_model = api.model('Amenity_Admin', {
    'name': fields.String(required=True, description='Name of the amenity')
})

place_input_admin_model = api.model('PlaceInput_Admin', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

review_admin_model = api.model('Review_Admin', {
    'text': fields.String(required=True, description='Content of the review'),
    'rating': fields.Integer(required=False, description='Rating (optional)')
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_admin_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Bad request: Email already registered, missing field, or invalid format')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'message': 'User successfully created'
        }, 201


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_update_admin_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Bad request: invalid input or email already registered')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Logic to update user details
        try:
            user.update(data)
            if 'password' in data and data['password']:
                user.hash_password(data['password'])
                user.save()

        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_admin_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json

        # Logic to create a new amenity
        try:
            new_amenity = facade.create_amenity(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_admin_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Bad request: Invalid name or missing field')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = request.json

        # Logic to update an amenity
        try:
            amenity.update(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_input_admin_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json

        # Logic to update the place
        try:
            facade.update_place(place_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Place updated successfully'}, 200

@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @api.expect(review_admin_model, validate=True)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """
        Update a specific review by ID.
        """
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json

        try:
            facade.update_review(review_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review by ID.
        """
        current_user = get_jwt_identity()

        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)

        # Vérifie que la review existe
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Deletion failed'}, 400

        return {'message': 'Review deleted successfully'}, 200
