from flask import jsonify
from sqlalchemy.orm.collections import InstrumentedList

def json_response(response):
    '''
        Returns a serializable version of an object, list of objects or
        InstrumentedList of objects.
    '''
    if type(response) is list or type(response) is InstrumentedList:
        return jsonify([item.serialized for item in response])
    else:
        return jsonify(response.serialized)