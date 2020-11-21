import firebase_admin
from firebase_admin import auth as fb_auth
from firebase_admin import storage as fb_stor
import json, os, base64
from io import BytesIO

class MockUser():
    def __init__(self, user_data):
        self.uid = user_data['uid']
        self.display_name = user_data['name']
        self.email = user_data['email']

class Firebase():
    def init_app(self, app):
        self.account_key_json = json.loads(app.config["FIREBASE_ACCOUNT_KEY_JSON"], strict=False)
        self.cred = firebase_admin.credentials.Certificate(self.account_key_json)
        self.project_id = app.config["FIREBASE_PROJECT_ID"]
        self.bucket_name = app.config["FIREBASE_BUCKET_NAME"]
        self.app = firebase_admin.initialize_app(self.cred, 
            {'projectId':self.project_id, '': self.bucket_name})
        self.bucket = fb_stor.bucket(self.bucket_name)
        self.auth = fb_auth.Client(self.app)
        self.config = app.config

    def verify_token(self, token):
        return self.auth.verify_id_token(token)

    def get_user(self, uid):
        if uid == self.config["FIREBASE_TEST_USER"]["uid"]:
            return self.config["FIREBASE_TEST_USER"]
        else:
            return self.auth.get_user(uid)
    
    def upload_image(self, file_base64):
        file_to_upload = BytesIO(base64.b64decode(file_base64))
        file_name = os.urandom(64).hex()
        blob = self.bucket.blob(file_name)
        blob.upload_from_file(file_to_upload, content_type='image/png')
        blob.make_public()
        return blob.public_url