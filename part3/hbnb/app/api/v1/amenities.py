from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Input/output model for Amenity
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """
    Collection resource for creating and listing amenities.
    """
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity.

        Validates the input and registers a new amenity with a name.
        """
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve all amenities.

        Returns:
            A list of all registered amenities.
        """
        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name
            } for a in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Item resource for retrieving or updating a single amenity.
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id (str): The unique ID of the amenity.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Bad request: Invalid name or missing field')
    def put(self, amenity_id):
        """
        Update an existing amenity.

        Args:
            amenity_id (str): The ID of the amenity to update.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        amenity_data = api.payload

        try:
            amenity.update(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
