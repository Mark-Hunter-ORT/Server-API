from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.utils import json_response, validate_required_properties
from app.models.mark_hunter import User_Category_Points, Category, Mark, Location, GPS_Location, Magnetic_Location
from app.models.mark_hunter import Content, Content_Images, User
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/test/', methods=['GET', 'PUT', 'DELETE'])
def test():
    return jsonify(request.current_user)

@api_blueprint.route('/api/location/', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        new_gps_location = GPS_Location(GPS_x=request.json["GPS"]["GPS_x"], GPS_y=request.json["GPS"]["GPS_y"])
        new_location = Location(GPS=new_gps_location, user_id=request.current_user['id'])
        if "magnetic" in request.json:
            new_magnetic_location = Magnetic_Location(magnetic_x=request.json['magnetic']['magnetic_x'],
            magnetic_y=request.json['magnetic']['magnetic_x'], magnetic_z=request.json['magnetic']['magnetic_z'])
            new_location.magnetic = new_magnetic_location
        db.session.add(new_location)
        db.session.commit()
        return json_response(new_location), 201
    query = db.session.query(Location).filter(Location.user_id == request.current_user['id']).all()
    return json_response(query), 200

@api_blueprint.route('/api/location/<id>/', methods=['GET', 'DELETE'])
def location_id(id):
    location = db.session.query(Location).filter(Location.id == id and Location.user_id == request.current_user['id'])[0]
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
    category = db.session.query(Category).filter(Category.id == id)[0]
    if request.method == 'GET':
        return json_response(category), 200
    if request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'category deleted'}), 200

@api_blueprint.route('/api/mark/', methods=['GET', 'POST'])
def mark():
    if request.method == 'POST':
        category = db.session.query(Category).filter(Category.name == request.json["category"])[0]
        if 'location_id' in request.json:
            location = db.session.query(Location).filter(Location.id == id and Location.user_id == request.current_user['id'])[0]
        else:
            gps_location = GPS_Location(GPS_x=request.json["location"]["GPS"]["GPS_x"], 
                                        GPS_y=request.json["location"]["GPS"]["GPS_y"])
            location = Location(GPS=gps_location, user_id=request.current_user['id'])
            if "magnetic" in request.json["location"]:
                location.magnetic = Magnetic_Location(magnetic_x=request.json["location"]['magnetic']['magnetic_x'],
                                                      magnetic_y=request.json["location"]['magnetic']['magnetic_x'], 
                                                      magnetic_z=request.json["location"]['magnetic']['magnetic_z'])
        new_mark = Mark(location=location, user_id=request.current_user['id'], category=category)
        db.session.add(new_mark)
        db.session.commit()
        return json_response(new_mark), 201
    query = db.session.query(Mark).all()
    return json_response(query), 200

@api_blueprint.route('/api/mark/<id>/', methods=['GET', 'DELETE'])
def mark_id(id):
    mark = db.session.query(Mark).filter(Mark.id == id)[0]
    if request.method == 'GET':
        return json_response(mark), 200
    if request.method == 'DELETE':
        db.session.delete(mark)
        db.session.commit()
        return jsonify({'message': 'category deleted'}), 200

@api_blueprint.route('/api/user/<id>/')
def user_id(id):
    return json_response(User(id)), 200