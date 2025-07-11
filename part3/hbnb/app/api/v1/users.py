from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for request validation and Swagger documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Bad request: Email already registered, missing field, or invalid format')
    def post(self):
        """
        Create a new user.
        ---
        tags:
          - Users
        description: >
            Registers a new user if the email is not already used.
        responses:
            201:
                description: User successfully created
            400:
                description: Email already exists or invalid data
        """
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'message': 'User successfully created'
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve all users.
        ---
        tags:
          - Users
        description: >
            Returns a list of all registered users with their basic details.
        responses:
            200:
                description: List of users retrieved successfully
        """
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve a user's details by ID.
        ---
        tags:
          - Users
        parameters:
          - in: path
            name: user_id
            required: true
            type: string
            description: The ID of the user
        responses:
            200:
                description: User details retrieved successfully
            404:
                description: User not found
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Bad request: invalid input or email already registered')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """
        Update an existing user's information.
        ---
        tags:
          - Users
        description: >
            Only the authenticated user can update their first and last name.
            Email and password updates are not allowed here.
        parameters:
          - in: path
            name: user_id
            required: true
            type: string
            description: The ID of the user to update
        responses:
            200:
                description: User successfully updated
            400:
                description: Invalid input or forbidden field
            403:
                description: Unauthorized action
            404:
                description: User not found
        """
        current_user = get_jwt_identity()
        user_data = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if user.id != current_user['id']:
            return {'error': 'Unauthorized action.'}, 403

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400
        try:
            user.update(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
