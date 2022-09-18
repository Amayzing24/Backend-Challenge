from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import or_
from flask_login import LoginManager
from flask_caching import Cache

## Initial configurations
DB_FILE = "clubreview.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'penn-labs-backend'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)

# Login manager to handle authentication
login_manager = LoginManager()
login_manager.init_app(app)

# Route cacher
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# Import authentication related routes
import auth

# Import data models
from models import *

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

# GET: fetches a list of all clubs and their associated data, response is cached for 5 minutes
# POST: creates a new club with specified parameters, requires the following parameters
#   code: club code
#   name: club name
#   description: club description (optional)
#   tags: tags associated with this club (optional)
@app.route('/api/clubs', methods=['GET', 'POST'])
@cache.cached(timeout=300, key_prefix='all_clubs')
def clubs():
    if request.method == 'GET':
        return jsonify([club.as_json() for club in Club.query.all()])
    else:
        request_data = request.get_json()

        # if data not proper
        if request_data == None or "code" not in request_data or "name" not in request_data:
            return "400 BAD REQUEST"

        # checks for duplicate name or code
        if Club.query.filter(or_(func.lower(Club.name) == func.lower(request_data["name"]), func.lower(Club.code) == func.lower(request_data["code"]))).first():
            return "400 BAD REQUEST"

        club = Club(code=request_data['code'].lower(), name=request_data['name'])

        if 'tags' in request_data:
            tags = process_tags(request_data['tags'])
            club.tags = tags

        if 'description' in request_data:
            club.description = request_data['description']

        db.session.add(club)

        db.session.commit()

        return "200 OK"


# GET: fetches all clubs whose name contains the query (case ignorant)
# PUT: modifies the club that has code of the query (case matters), can modify one or more of the following
#   name: new name of the club
#   tags: new tags associated with this club
#   description: new description of the club
@app.route('/api/clubs/<search>', methods=['GET', 'PUT'])
def club(search):
    if request.method == 'GET':
        clubs = Club.query.filter(func.lower(Club.name).contains(func.lower(search)))
        clubs = [club.as_json() for club in clubs]
        if len(clubs) == 0:
            return "204 NO CONTENT"
        return jsonify(clubs)
    else:
        request_data = request.get_json()

        # if data not proper
        if request_data == None or "code" in request_data or "favorited" in request_data:
            return "405 METHOD NOT ALLOWED"

        club = Club.query.filter(func.lower(search) == Club.code).first()

        # if club does not exist
        if club == None:
            return "404 NOT FOUND"

        if "name" in request_data:
            club.name = request_data['name']
        if "tags" in request_data:
            tags = process_tags(request_data['tags'])
            club.tags = tags
        if "description" in request_data:
            club.description = request_data['description']
        db.session.commit()

        return "200 OK"

# GET: fetches data for user with the provided username
@app.route('/api/users/<username>', methods=['GET'])
def user(username):
    user = User.query.filter(func.lower(User.user) == func.lower(username)).first()
    if user == None:
        return "404 NOT FOUND"
    return jsonify(user.as_json())

# GET: fetches all tags and the number of clubs associated with each tag, response is cached for 5 minutes
@app.route('/api/tags', methods=['GET'])
@cache.cached(timeout=300, key_prefix='all_tags')
def get_tags():
    tags = [tag.as_json(False) for tag in Tag.query.all()]
    return jsonify(tags)

# GET: given a tag name, fetches tag and clubs associated with that tag, response for a specific tag is memoized for 5 minutes
@app.route('/api/tags/<tagname>', methods=['GET'])
@cache.memoize(timeout=300)
def get_specific_tag(tagname):
    tag = Tag.query.filter(func.lower(Tag.name) == func.lower(tagname)).first()
    if tag == None:
        return "404 NOT FOUND"
    return jsonify(tag.as_json(True))

# helper function that takes in tag names and output tag objects from model for those names
# for tags with a name not yet used, creates new tag tag objects and adds to database
def process_tags(tag_names):
    tags = []
    for tag in tag_names:
        found = False
        for t in Tag.query.all():
            if tag == t.name:
                found = True
                tags.append(t)
                break
        if not found:
            new_tag = Tag(name=tag)
            db.session.add(new_tag)
            tags.append(new_tag)
    db.session.commit()
    return tags

if __name__ == '__main__':
    app.run()
