from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

# Create Blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

# User Registration


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expects JSON: {"username": "test", "email": "test@test.com", "password": "password123"}
    """
    data = request.get_json()

    # Validate input
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if the user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already in use"}), 409

    # Hash password
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # Create and save new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User Login


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    Expects JSON: {"email": "test@test.com", "password": "password123"}
    """
    data = request.get_json()

    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Fetch user by email
    user = User.query.filter_by(email=data['email']).first()

    # Check password
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200

# Protected Route Example


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Get user profile (protected route).
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }), 200
