import firebase_admin
from firebase_admin import auth as fb_auth
import json

class Firebase():
    def __init__(self, app):
        self.account_key_json = json.loads(app.config["FIREBASE_ACCOUNT_KEY_JSON"], strict=False)
        self.cred = firebase_admin.credentials.Certificate(self.account_key_json)
        self.project_id = app.config["FIREBASE_PROJECT_ID"]
        self.app = firebase_admin.initialize_app(self.cred, {'projectId':self.project_id})
        self.auth = fb_auth.Client(self.app)


    def verify_token(self, token):
        return self.auth.verify_id_token(token)