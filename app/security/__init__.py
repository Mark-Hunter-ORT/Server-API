from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from app.models.mark_hunter import User
from app import db
from app import login
from .exceptions import InvalidCredentialsException, UsernameNotFoundException
import os

def generate_new_user(username, token, email, google_id):
    token_hash = generate_password_hash(token)
    new_user = User(
        username=username,
        email=email,
        oauth_token=token_hash,
        google_id=google_id
    )
    db.session.add(new_user)
    db.session.commit()

def change_token(user, old_token, new_token):
    if check_user_credentials(user, old_token):
        new_password_hash = generate_password_hash(new_token)
        user.password = new_password_hash
    else:
        raise InvalidCredentialsException("Username/Password invalid.")

def check_user_credentials(user, token):
    return check_password_hash(user.oauth_token, token)

def check_username_availability(username):
    if db.session.query(User).filter(User.username == username):
        return False
    else:
        return True

def check_email_availability(email):
    if db.session.query(User).filter(User.email == email):
        return False
    else:
        return True

def get_user_from_credentials(username, token):
    '''
        Verifies that the given credentials are valid and if they are, returns the
        corresponding user object.
    '''
    user = User.query.filter(User.username == username).first()
    if not user:
        abort(404, "User not found")
    if check_user_credentials(user, token):
        return user
    else:
        return None

@login.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()

