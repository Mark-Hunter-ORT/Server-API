from enum import Enum
from flask_login import UserMixin
from app import db

class ApiModel():
    required_properties = []
    @classmethod
    def verifyProperties(cls, content):
        return all([x in content for x in cls.required_properties])

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    google_id = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    oauth_token = db.Column(db.Unicode(255), nullable=True, server_default=u'', unique=True)

class User_Followings(db.Model):
    __tablename__ = 'user_followings'
    id = db.Column(db.Integer, primary_key=True)

    hunter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    marker_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User_Category_Points(db.Model):
    __tablename__ = 'user_category_points'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    points = db.Column(db.Integer)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255), nullable=False, unique=True)

class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'))

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    GPS_id = db.Column(db.Integer, db.ForeignKey('GPS.id'))
    magnetic_id = db.Column(db.Integer, db.ForeignKey('magnetic.id'))

class GPS_Location(db.Model):
    __tablename__ = 'GPS'
    id = db.Column(db.Integer, primary_key=True)

    GPS_X = db.Column(db.Float, nullable=False)
    GPS_Y = db.Column(db.Float, nullable=False)

class Magnetic_Location(db.Model):
    __tablename__ = 'magnetic'
    id = db.Column(db.Integer, primary_key=True)

    magnetic_X = db.Column(db.Float, nullable=False)
    magnetic_Y = db.Column(db.Float, nullable=False)
    magnetic_Z = db.Column(db.Float, nullable=False)

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Unicode(1024), nullable=True, server_default=u'')

class Content_Images(db.Model):
    __tablename__ = 'content_images'
    id = db.Column(db.Integer, primary_key=True)

    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'))
    image_url = db.Column(db.Unicode(512), nullable=False)