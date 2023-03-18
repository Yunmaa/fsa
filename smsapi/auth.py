from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .exts import db
from .models import User, Student
from .schemas import UserSchema
from .routes import student_ns

auth_ns = Namespace('Auth', description='Authentication Operations')
user_schema = UserSchema()

auth_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})


# Registration
@auth_ns.route('/register')
class RegistrationResource(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400

        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first() is not None:
            return {"message": "Email already exists"}, 409

        new_user = User(email=email, password_hash=password)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201


# Authentication
@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400

        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return {"message": "Invalid email or password"}, 401

        # Create a JWT access token
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200


# Access control using the jwt_required decorator
@student_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return {'Message': f'Welcome, {user.email}'}, 200


# api.add_namespace(auth_ns, path='/auth')

