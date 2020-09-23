# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()

