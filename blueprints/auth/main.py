
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required,
    create_access_token, create_refresh_token, 
    get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
    )

from app import jwt_app

auth_module = Blueprint('auth_module', __name__, template_folder="templated")

# Create and configure the JWT app


@auth_module.route('/login')
def login():
    return 'Login view'


@auth_module.route('/auth/authenticate', methods=['POST'])
def authenticator():
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Missing JSON data'})

    # If the necessary values are not send as JSON, an exception will be returned.
    try:
        # This can be treated as the username or email
        user_id = request.json.get('user_id', None)
        password =  request.json.get('password', None)
    except:
        return jsonify({'status': 'error', 'message': 'Missing user_id or password'})

    if user_id != 'test' or password != 'test':
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})

    # If everything was OKAI, we create and store the tokens in HTTP only cookies
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)

    response = jsonify({'status': 'success'})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@auth_module.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    access_token = create_access_token(identity=get_jwt_identity())
    response = jsonify({'status': 'success', 'message': 'Token has been refreshed'})

    return response


# Logout
@auth_module.route('/token/remove', methods=['POST'])
def logout():
    response = jsonify({'status': 'success', 'message': 'Logout has been successful'})
    unset_jwt_cookies(response)

    return response


@auth_module.route('/api/test', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()

    return jsonify({'user_id': username})


