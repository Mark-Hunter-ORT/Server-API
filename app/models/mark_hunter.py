from enum import Enum
from flask_login import UserMixin
from flask import abort, request
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
    category = db.relationship('Category')
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
    content = db.relationship('Content')

    required_properties = ['category_id', 'location_id', 'content_id']

    @property
    def serialized(self):
        # data = {
        #     'user_id': self.user_id,
        #     'category': self.category.serialized,
        #     'location': self.location.serialized
        # }
        # if self.user_id == request.current_user['uid']:
        #     data['content'] = self.content.serialized
        # return data
        return {
            'user_id': self.user_id,
            'category': self.category.serialized,
            'location': self.location.serialized,
            'content': self.content.serialized,
            'id': self.id
        }

    @property
    def serialized_revealed(self):
        return {
            'user_id': self.user_id,
            'category': self.category.serialized,
            'location': self.location.serialized,
            'content': self.content.serialized,
            'id': self.id
        }
    
    def get_coordinates(self):
        return (self.location.GPS.GPS_y, self.location.GPS.GPS_x)

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


class Content_Images(db.Model, ApiModel):
    __tablename__ = 'content_images'
    id = db.Column(db.Integer, primary_key=True)

    content_id = db.Column(db.Integer, db.ForeignKey('contents.id'))
    content = db.relationship('Content')
    image_url = db.Column(db.Unicode(512), nullable=False)

    required_properties = ['content_id', 'image_url']

class Content(db.Model, ApiModel):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Unicode(1024), nullable=True, server_default=u'')
    images = db.relationship('Content_Images')

    def add_image(self, file_b64):
        file_url = firebase.upload_image(file_b64)
        image = Content_Images(content=self, image_url=file_url)
        db.session.add(image)
        
    @property
    def serialized(self):
        return {
            'id': self.id,
            'text': self.text,
            'images': [image.image_url for image in self.images]
        }

class UserDB(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Unicode(64))
    username = db.Column(db.Unicode(64))

class User():
    def __init__(self, uid):
        user_db = db.session.query(UserDB).filter(UserDB.user_id == uid).first()
        firebase_user = firebase.get_user(uid)
        self.username = user_db.username
        self.name = firebase_user.display_name
        self.email = firebase_user.email
        self.uid = uid
        followers = db.session.query(User_Followings).filter(User_Followings.marker_id == uid).all()
        self.followers = [follower.hunter_id for follower in followers]
        followings = db.session.query(User_Followings).filter(User_Followings.hunter_id == uid).all()
        self.following = [following.marker_id for following in followings]
        points = db.session.query(User_Category_Points).filter(User_Category_Points.user_id == uid).all()
        self.points = {}
        for point in points:
            self.points[point.category.name] = point.points
    
    def follow(self, hunter_uid):
        if hunter_uid in self.followers:
            abort(400, "User {} already following user {}".format(hunter_uid, self.uid))
        else:
            new_user_following = User_Followings(marker_id=self.uid, hunter_id=hunter_uid)
            self.followers.append(hunter_uid)
            db.session.add(new_user_following)

    def unfollow(self, hunter_uid):
        if hunter_uid not in self.followers:
            abort(400, "User {} is not following user {}".format(hunter_uid, self.uid))
        else:
            user_following = db.session.query(User_Followings).filter(User_Followings.marker_id == self.uid and
                                        User_Followings.hunter_id == hunter_uid).first()
            db.session.delete(user_following)
        
    def add_points(self, category_name, points):
        category = db.session.query(Category).filter(Category.name == category_name).first()
        category_points = db.session.query(User_Category_Points).filter(User_Category_Points.user_id == self.uid and
                                        User_Category_Points.category_id == category.id).first()
        if category_points is None:
            category_points = User_Category_Points(user_id=self.uid, category_id=category.id, points=0)
        category_points.points += points
        self.points[category_name] = category_points.points
        db.session.add(category_points)

    @property
    def serialized(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'followers': self.followers,
            'following': self.following,
            'points': self.points,
            'username': self.username
        }