from enum import Enum
from flask_login import UserMixin
from flask import abort
from app import db
from app import fb as firebase

class ApiModel():
    required_properties = []
    @classmethod
    def verifyProperties(cls, content):
        return all([x in content for x in cls.required_properties])

    @property
    def serialized(self):
        abort(500, "The class {} does has the 'serialized' method implemented".format(self.__class__.__name__))

class User_Followings(db.Model, ApiModel):
    __tablename__ = 'user_followings'
    id = db.Column(db.Integer, primary_key=True)

    hunter_id = db.Column(db.Unicode(64))
    marker_id = db.Column(db.Unicode(64))

    required_properties = ['hunter_id', 'marker_id']

class User_Category_Points(db.Model, ApiModel):
    __tablename__ = 'user_category_points'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Unicode(64))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    points = db.Column(db.Integer)

    required_properties = ['user_id', 'category_id']

class Category(db.Model, ApiModel):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255), nullable=False, unique=True)

    required_properties = ['name']

    @property
    def serialized(self):
        return self.name

class Mark(db.Model, ApiModel):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Unicode(64))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category')
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Location')
    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'))

    required_properties = ['category_id', 'location_id', 'content_id']

    @property
    def serialized(self):
        return {
            'user_id': self.user_id,
            'category': self.category.serialized,
            'location': self.location.serialized
        }

class Location(db.Model, ApiModel):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Unicode(64))
    GPS_id = db.Column(db.Integer, db.ForeignKey('GPS.id'))
    GPS = db.relationship('GPS_Location')
    magnetic_id = db.Column(db.Integer, db.ForeignKey('magnetic.id'))
    magnetic = db.relationship('Magnetic_Location')

    required_properties = ['GPS_id']

    @property
    def serialized(self):
        data = {
            'id': self.id,
            'GPS': self.GPS.serialized,
            'user_id': self.user_id
        }
        if self.magnetic_id:
            data['magnetic'] = self.magnetic.serialized
        return data

class GPS_Location(db.Model, ApiModel):
    __tablename__ = 'GPS'
    id = db.Column(db.Integer, primary_key=True)

    GPS_x = db.Column(db.Float, nullable=False)
    GPS_y = db.Column(db.Float, nullable=False)

    required_properties = ['GPS_x', 'GPS_y']

    @property
    def serialized(self):
        return {
            'id': self.id,
            'GPS_x': self.GPS_x,
            'GPS_y': self.GPS_y
        }

class Magnetic_Location(db.Model, ApiModel):
    __tablename__ = 'magnetic'
    id = db.Column(db.Integer, primary_key=True)

    magnetic_x = db.Column(db.Float, nullable=False)
    magnetic_y = db.Column(db.Float, nullable=False)
    magnetic_z = db.Column(db.Float, nullable=False)

    required_properties = ['magnetic_x', 'magnetic_y', 'magnetic_z']

    @property
    def serialized(self):
        return {
            'id': self.id,
            'magnetic_x': self.magnetic_x,
            'magnetic_y': self.magnetic_y,
            'magnetic_z': self.magnetic_z
        }

class Content(db.Model, ApiModel):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Unicode(1024), nullable=True, server_default=u'')

    required_properties = ['text']

class Content_Images(db.Model, ApiModel):
    __tablename__ = 'content_images'
    id = db.Column(db.Integer, primary_key=True)

    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'))
    image_url = db.Column(db.Unicode(512), nullable=False)

    required_properties = ['content_id', 'image_url']

class User():
    def __init__(self, uid):
        firebase_user = firebase.get_user(uid)
        self.name = firebase_user.display_name
        self.email = firebase_user.email
        self.uid = uid
    
    @property
    def serialized(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email
        }