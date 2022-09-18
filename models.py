from app import db
from flask_login import UserMixin

# Your database models should go here.
# Check out the Flask-SQLAlchemy quickstart for some good docs!
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

# tables for many-to-many relationships and back referencing
tag_club = db.Table('tags',
                    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
user_club_favorite = db.Table('users_favorites',
                              db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

# club data type
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=tag_club, backref=db.backref('clubs', lazy=True), lazy=True)
    favorited = db.relationship('User', secondary=user_club_favorite, backref=db.backref('favorites', lazy=True), lazy=True)

    def __repr__(self):
        return f'<Club: {self.name}>'

    def as_json(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "favorited": len(self.favorited),
            "tags": [tag.name for tag in self.tags]
        }


# tag data type
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag: {self.name}>'

    def as_json(self, club_names):
        out = {
            "name": self.name,
            "count": len(self.clubs)
        }
        if club_names:
            out["clubs"] = [club.name for club in self.clubs]
        return out


# user data type
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer)
    email = db.Column(db.String(30))

    def __repr__(self):
        return f'<User: {self.user}>'

    # does not return the password for security purposes
    def as_json(self):
        return {
            "user": self.user,
            "name": self.name,
            "year": self.year,
            "email": self.email,
            "favorites": [club.name for club in self.favorites]
        }
