from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, abort
from flask_login import login_user, login_required, current_user
from app import db
from app.utils import json_response
from app.security import get_user_from_credentials
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/api/login/", methods=["POST"])
def login():
    user = get_user_from_credentials(request.json["username"],request.json["oauth_token"])
    if user:
        login_user(user)
        return "OK"
    else:
        abort(403)
