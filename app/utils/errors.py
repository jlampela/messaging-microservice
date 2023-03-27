from flask import jsonify, make_response
from jsonschema import ValidationError


class ServiceErrors(Exception):
    """
    This is make to handle all the errors occured
    """
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

    @property
    def response(self):
        return make_response(jsonify({'error' : self.message, 'code' : self.code}), self.code)


def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message, 'code' : 400}), 400)
    # handle other "Bad Request"-errors
    return error