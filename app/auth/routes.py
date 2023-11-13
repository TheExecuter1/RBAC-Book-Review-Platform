from flask import Blueprint, request, jsonify
from app.models import User
from app import db, bcrypt, jwt
from flask_jwt_extended import create_access_token , jwt_required , get_jwt_identity
from app.auth.decorators import admin_required


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate presence of username and password
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'Regular User') 
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Validate username and password length
    if len(username) < 3 or len(password) < 6:
        return jsonify({'message': 'Username must be at least 3 characters and password at least 6 characters long'}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    user = User(username=username, password=password, role=role)
    #user.password = data['password']
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.verify_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid username or password'}), 401


@auth_blueprint.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([{'username': user.username, 'role': user.role} for user in users])