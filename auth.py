from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from __main__ import app
from app import db
from models import *

# Contains routes dealing with user authentication

# POST: creates a new user
# requires the following to be included in json body
#   user: unique username
#   name: student's name
#   password: user's password
#   year: student's year (optional)
#   email: student's email (optional)
@app.route('/auth/signup', methods=['POST'])
def signup():
    request_data = request.get_json()

    if not request_data or "user" not in request_data or "name" not in request_data or "password" not in request_data:
        return "400 BAD REQUEST"

    if User.query.filter(User.user == request_data["user"]).first():
        return "400 BAD REQUEST"

    # Stores the hashed password
    user = User(user=request_data['user'], name=request_data['name'], password=generate_password_hash(request_data['password'], method='sha256'))

    if ('year' in request_data):
        user.year = request_data['year']
    if ('email' in request_data):
        user.email = request_data['email']
    
    db.session.add(user)
    db.session.commit()

    return "200 OK"

# POST: logs in a user
# overrides the current user
# requires the following
#   user: username
#   password: password (must be correct)
@app.route('/auth/login', methods=['POST'])
def login():
    request_data = request.get_json()

    if not request_data or "user" not in request_data or "password" not in request_data:
        return "400 BAD REQUEST"

    user = User.query.filter(User.user == request_data["user"]).first()

    # Checks if username and password matches using hashing
    if not user or not check_password_hash(user.password, request_data["password"]):
        return "400 BAD REQUEST"

    login_user(user)
    return "200 OK"

# POST: logs out the current user
# requires a user to be currently logged in
@app.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return "200 OK"

# PUT: modifies data of currently logged in user, requires login
# can modify one or more of the following:
#   year of the user
#   email of the user
#   password of the user
#   club to be added to user's favorited list
@app.route('/auth/modify', methods=['PUT'])
@login_required
def modify_user():
    request_data = request.get_json()
    if 'year' in request_data:
        current_user.year = request_data['year']
    if 'email' in request_data:
        current_user.email = request_data['email']
    if 'password' in request_data:
        current_user.password = generate_password_hash(request_data['password'], method='sha256')
    if 'club' in request_data:
        club = Club.query.filter(Club.code == request_data['club']).first()
        if club == None:
            return "404 NOT FOUND"
        current_user.favorites.append(club)
    db.session.commit()
    return "200 OK"

# GET: gets the information of the currently logged in user
# requires user to be logged in
@app.route('/auth/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify(current_user.as_json())