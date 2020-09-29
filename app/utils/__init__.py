from flask import jsonify, abort
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

def validate_required_properties(cls, request):
    '''
        Validates that the request received has all of the properties required to
        create the given object.
    '''
    if not cls.verifyProperties(request.json):
        return abort(400, "Required properties: "+", ".join(cls.required_properties))