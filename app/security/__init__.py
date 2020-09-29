from flask import abort, request
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError
from .exceptions import InvalidCredentialsException, UsernameNotFoundException, TokenHeaderNotFoundException
import os

TOKEN_HEADER_KEY = 'User-Token'

class Security():
    def __init__(self, app, firebase):
        self.firebase = firebase
        self.app = app

    def validate_token(self, headers):
        token = headers.get(TOKEN_HEADER_KEY)
        user_uid = None
        if token is None:
            abort(401, "Must include '{}' header with token to authenticate request.".format(TOKEN_HEADER_KEY))
        try:
            user = self.firebase.verify_token(token)
            setattr(request, "current_user", user)
        except ExpiredIdTokenError:
            abort(401, "Provided token is expired.")
        except InvalidIdTokenError:
            if token == self.app.config["FIREBASE_TEST_TOKEN"]:
                setattr(request, "current_user", self.app.config["FIREBASE_TEST_USER"])
            else:
                abort(401, "Provided token is invalid.")


