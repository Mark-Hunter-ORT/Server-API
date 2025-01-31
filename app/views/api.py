from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app import fb as firebase
from app.utils import json_response, validate_required_properties
from app.models.mark_hunter import User_Category_Points, Category, Mark, Location, GPS_Location, Magnetic_Location
from app.models.mark_hunter import Content, Content_Images, User, UserDB, UserNotFound
import geopy.distance
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/test/')
def test():
    return jsonify(request.current_user)

@api_blueprint.route('/api/location/', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        new_gps_location = GPS_Location(GPS_x=request.json["GPS"]["GPS_x"], GPS_y=request.json["GPS"]["GPS_y"])
        new_location = Location(GPS=new_gps_location, user_id=request.current_user['uid'])
        if "magnetic" in request.json:
            new_magnetic_location = Magnetic_Location(magnetic_x=request.json['magnetic']['magnetic_x'],
            magnetic_y=request.json['magnetic']['magnetic_x'], magnetic_z=request.json['magnetic']['magnetic_z'])
            new_location.magnetic = new_magnetic_location
        db.session.add(new_location)
        db.session.commit()
        return json_response(new_location), 201
    query = db.session.query(Location).filter(Location.user_id == request.current_user['uid']).all()
    return json_response(query), 200

@api_blueprint.route('/api/location/<id>/', methods=['GET', 'DELETE'])
def location_id(id):
    location = db.session.query(Location).filter(Location.id == id and 
                                        Location.user_id == request.current_user['uid']).first()
    if request.method == 'GET':
        return json_response(location), 200
    if request.method == 'DELETE':
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'location deleted'}), 200
    
@api_blueprint.route('/api/category/', methods=['GET', 'POST'])
def category():
    if request.method == 'POST':
        new_category = Category(name=request.json["name"])
        db.session.add(new_category)
        db.session.commit()
        return json_response(new_category), 201
    query = db.session.query(Category).all()
    return json_response(query), 200

@api_blueprint.route('/api/category/<id>/', methods=['GET', 'DELETE'])
def category_id(id):
    category = db.session.query(Category).filter(Category.id == id).first()
    if request.method == 'GET':
        return json_response(category), 200
    if request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'category deleted'}), 200

@api_blueprint.route('/api/mark/', methods=['GET', 'POST'])
def mark():
    User.clear_cached_user()
    if request.method == 'POST':
        
        marks_too_close = Mark.get_marks_by_distance(request.json["location"]["GPS"]["GPS_x"],
                                                     request.json["location"]["GPS"]["GPS_y"], 5)
        if marks_too_close:
            return "This mark is too close to another mark.", 400

        category = db.session.query(Category).filter(Category.name == request.json["category"]).first()
        if 'location_id' in request.json:
            location = db.session.query(Location).filter(Location.id == id and 
                                                    Location.user_id == request.current_user['uid']).first()
        else:
            gps_location = GPS_Location(GPS_x=request.json["location"]["GPS"]["GPS_x"], 
                                        GPS_y=request.json["location"]["GPS"]["GPS_y"])
            location = Location(GPS=gps_location, user_id=request.current_user['uid'])
            if "magnetic" in request.json["location"]:
                location.magnetic = Magnetic_Location(magnetic_x=request.json["location"]['magnetic']['magnetic_x'],
                                                      magnetic_y=request.json["location"]['magnetic']['magnetic_x'], 
                                                      magnetic_z=request.json["location"]['magnetic']['magnetic_z'])
        if 'content_id' in request.json:
            content = db.session.query(Content).filter(Content.id == id).first()
        else:
            content = Content(text=request.json['content']['text'])
            for f in request.json['content']['files']:
                content.add_image(f)
        new_mark = Mark(location=location, user_id=request.current_user['uid'], category=category, content=content)
        db.session.add(new_mark)
        db.session.commit()
        return json_response(new_mark), 201
    query = db.session.query(Mark).all()
    return json_response(query), 200

@api_blueprint.route('/api/mark/<lat>/<lon>/<distance>/')
def mark_by_coords(lat, lon, distance):
    User.clear_cached_user()
    marks_in_range = Mark.get_marks_by_distance(float(lon), float(lat), float(distance))
    return json_response(marks_in_range), 200

@api_blueprint.route('/api/mark/<id>/', methods=['GET', 'DELETE'])
def mark_id(id):
    User.clear_cached_user()
    mark = db.session.query(Mark).filter(Mark.id == id)[0]
    if request.method == 'GET':
        return json_response(mark), 200
    if request.method == 'DELETE':
        db.session.delete(mark)
        db.session.commit()
        return jsonify({'message': 'mark deleted'}), 200

@api_blueprint.route('/api/user/<id>/')
def user_id(id):
    try:
        return json_response(User(id)), 200
    except UserNotFound:
        return 'User with id {} not found'.format(id), 404

@api_blueprint.route('/api/user/<id>/follow/', methods=['POST'])
def user_follow(id):
    marker_user = User(id)
    marker_user.follow(request.current_user['uid'])
    db.session.commit()
    return 'OK', 200

@api_blueprint.route('/api/user/', methods=['GET', 'POST'])
def user_post():
    try:
        user = User(request.current_user['uid'])
        if request.method == 'POST':
            return 'User already registered.', 400
        else:
            return json_response(user), 200
    except UserNotFound:
        if request.method == 'POST':
            user_db = UserDB(user_id=request.current_user['uid'], username=request.json["username"])
            db.session.add(user_db)
            db.session.commit()
            return json_response(User(request.current_user['uid'])), 201
        else:
            return 'User not found', 404

@api_blueprint.route('/api/user/followings/')
def user_followings():
    try:
        user = User(request.current_user['uid'])
        user_follows = [User(uid) for uid in user.following]
        followings = [{'uid': follow.uid, 'username': follow.username} for follow in user_follows]
        return jsonify(followings), 200
    except UserNotFound:
        return 'User with id {} not found'.format(id), 404

@api_blueprint.route('/api/user/<id>/unfollow/', methods=['DELETE'])
def user_unfollow(id):
    marker_user = User(id)
    marker_user.unfollow(request.current_user['uid'])
    db.session.commit()
    return 'DELETED', 200

@api_blueprint.route('/api/user/<id>/category/<cat_name>/add_points/', methods=['POST'])
def user_add_points(id, cat_name):
    user = User(id)
    user.add_points(cat_name, request.json['points'])
    db.session.commit()
    return json_response(user)

# @api_blueprint.route('/api/content/', methods=['GET','POST'])
# def content():
#     if request.method == 'POST':
#         content = Content(text=request.json['text'])
#         for f in request.json['files']:
#             content.add_image(f)
#         db.session.add(content)
#         db.session.commit()
#         return json_response(content), 201
#     contents = db.session.query(Content).all()
#     return json_response(contents), 200

        