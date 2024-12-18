from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from src import db, blacklist
from src.models import User
from sqlalchemy.exc import IntegrityError


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

    # Validate JSON and input data
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if the email is already in use
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already in use"}), 409

    # Hash the password
    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256', salt_length=16)

    # Create and save the new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409
    except Exception as e:
        db.session.rollback()
        # Return the error for debugging
        return jsonify({"error": str(e)}), 500

    # Generate JWT token in register route
    access_token = create_access_token(identity=str(new_user.id))

    # Return success message and JWT token
    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token
    }), 201

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

    # Generate JWT token in login route
    access_token = create_access_token(identity=str(user.id))

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
    user_id = get_jwt_identity()  # Retrieves the identity as a string
    # Convert back to integer for database lookup
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token), 200

# Logout route


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout a user by blacklisting their token.
    """
    jti = get_jwt()["jti"]  # Retrieve the JWT ID
    blacklist.add(jti)      # Add the token to the blacklist
    return jsonify({"message": "Successfully logged out"}), 200


# Revoke Token Route
@auth_bp.route('/revoke', methods=['POST'])
@jwt_required()
def revoke():
    """
    Revoke a token by adding its JTI to the blacklist.
    Admin or authorized user can revoke any specific token.
    Expects JSON: {"jti": "<token_jti>"}
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("jti"):
        return jsonify({"error": "Token JTI is required"}), 400

    jti_to_revoke = data["jti"]

    # Optionally, you can add a check if the user is an admin
    # Example: if not is_admin(current_user_id): return 403 error

    blacklist.add(jti_to_revoke)
    return jsonify({"message": f"Token with JTI {jti_to_revoke} has been revoked"}), 200
