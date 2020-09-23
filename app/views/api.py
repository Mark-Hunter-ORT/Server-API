from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.utils import json_response
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/test/', methods=['GET', 'PUT', 'DELETE'])
def test():
    return jsonify(request.current_user)

