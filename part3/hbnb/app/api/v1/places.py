from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# --------------------------------------------
# Nested models (owner, amenity, review)
# --------------------------------------------
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# --------------------------------------------
# Input model (used for POST/PUT)
# --------------------------------------------
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

# --------------------------------------------
# Output model (GET)
# --------------------------------------------
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    """
    Collection resource for creating and listing places.
    """
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new place.
        ---
        tags:
          - Places
        description: >
            Creates a new place associated with the current user as owner.
            Requires authentication. Amenities are linked by ID.
        responses:
            201:
                description: Place successfully created
            400:
                description: Invalid input data
        """

        current_user = get_jwt_identity()
        place_data = api.payload

        place_data['owner_id'] = current_user['id']

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner.id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve all places.
        ---
        tags:
          - Places
        description: >
            Retrieves a list of all places with owner ID only.
        responses:
            200:
                description: List of places retrieved successfully
        """
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'price': p.price,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'owner_id': p.owner.id
            } for p in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Item resource for retrieving or updating a single place.
    """
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve a place by ID.
        ---
        tags:
          - Places
        description: >
            Returns detailed information about a place, including:
            owner info, amenities, and reviews.
        parameters:
          - in: path
            name: place_id
            required: true
            type: string
            description: The ID of the place
        responses:
            200:
                description: Place details retrieved successfully
            404:
                description: Place not found
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {'id': a.id, 'name': a.name} for a in place.amenities
            ],
            'reviews': [
                {
                    'id': r.id,
                    'text': r.text,
                    'rating': r.rating,
                    'user_id': r.user.id
                } for r in place.reviews
            ]
        }, 200

    @api.expect(place_input_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """
        Update an existing place.
        ---
        tags:
          - Places
        description: >
            Updates an existing place. Only the owner of the place
            can perform the update. Amenities list is fully replaced
            if provided. Owner ID cannot be changed.
        parameters:
          - in: path
            name: place_id
            required: true
            type: string
            description: The ID of the place
        responses:
            200:
                description: Place updated successfully
            400:
                description: Invalid input data
            403:
                description: Unauthorized action
            404:
                description: Place not found
        """
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner.id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Place updated successfully'}, 200
