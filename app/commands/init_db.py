# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.mark_hunter import User
from app.security import generate_new_user

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Add users
    # Normal user
    generate_new_user(
        current_app.config["INITIAL_USERS"]["user"]["username"],
        current_app.config["INITIAL_USERS"]["user"]["oauth_token"],
        current_app.config["INITIAL_USERS"]["user"]["email"],
        current_app.config["INITIAL_USERS"]["user"]["google_id"])

    # Save to DB
    db.session.commit()

