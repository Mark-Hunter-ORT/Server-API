from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.utils import json_response
api_blueprint = Blueprint('api', __name__)

# @api_blueprint.route('/api/team/<id>/', methods=['GET', 'PUT', 'DELETE'])
# @login_required
# def teamId(id):
#     team = db.session.query(Team).filter(Team.id == id)[0]
#     if request.method == 'GET':
#         return json_response(team), 200
#     if request.method == 'PUT':
#         validate_required_properties(Team,request)
#         team.club = request.json['club']
#         team.manager = request.json['manager']
#         db.session.commit()
#         return json_response(team), 200
#     if request.method == 'DELETE':
#         db.session.delete(team)
#         db.session.commit()
#         return jsonify({'message': 'team deleted'}), 200

