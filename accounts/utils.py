import  json
import requests
import json
import mysql.connector 
import jwt
import hashlib
import bcrypt
from mysql.connector import Error
import datetime
from flask import Flask
import bcrypt  
from flask_bcrypt import Bcrypt 



app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdbcdskj'
bcrypt = Bcrypt(app)




def registation_utils(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (name, email, hashed_password))
        connection.commit()
        return {'message': 'User registered successfully!',"status_code":201}
    except mysql.connector.Error as err:
        return {'message': str(err),"status_code":400}
    finally:
        cursor.close()
        connection.close()
    



def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="camcom",
            passwd="Camcom@123",
            database="User"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def generate_access_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow()
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def generate_refresh_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    refresh_token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow()
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "UPDATE users SET refresh_token = %s WHERE id = %s"
    cursor.execute(query, (refresh_token, user_id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return refresh_token

def decode_token(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded_token, None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired, please refresh it'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'


