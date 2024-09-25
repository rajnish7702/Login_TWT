from flask import Blueprint, request, Response,jsonify
from .utils import *
from flask_bcrypt import Bcrypt  
from passlib.hash import bcrypt


views = Blueprint('views', __name__)

@views.route("/registration", methods=["POST"])
def registration():
    data = request.json
    return registation_utils(data)

@views.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        decoded_token, error = decode_token(token)
        if error:
            return jsonify({'message': error}), 401
        return jsonify({'message': 'Access granted', 'user_id': decoded_token['user_id']}), 200
    return jsonify({'message': 'Token is missing!'}), 401


@views.route("/login",methods=["POST"])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    print(user)
    hashed_password = bcrypt.hash(password)

    if user and bcrypt.verify(password, user['password']):
    # if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

    
    
@views.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.json
    refresh_token = data.get('refresh_token')

    decoded_refresh_token, error = decode_token(refresh_token)
    if error:
        return jsonify({'message': error}), 401
    
    user_id = decoded_refresh_token['user_id']

    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT refresh_token FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result and result['refresh_token'] == refresh_token:
        new_access_token = generate_access_token(user_id)
        return jsonify({'access_token': new_access_token}), 200
    else:
        return jsonify({'message': 'Invalid refresh token'}), 401
