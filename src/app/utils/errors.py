from flask import jsonify

def unauthorized(message):
    response = jsonify({'status':'401', 'error':'unauthorized', 'message': message})
    response.status_code = 401
    return response


class ServiceErrors(Exception):
    """
    This is make to handle all the errors occured
    """
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message