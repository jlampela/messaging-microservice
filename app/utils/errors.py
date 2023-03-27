from flask import jsonify

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
        response = jsonify({'status': self.code, 
                            'error': self.message})
        response.status_code = self.code
        return response


from flask import make_response, jsonify
from jsonschema import ValidationError

def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message, 'code' : 400}), 400)
    # handle other "Bad Request"-errors
    return error