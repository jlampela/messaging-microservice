from flask import Flask
from flask_restful import Api

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#from flask_babel import Babel

from app.utils.errors import bad_request
from .config import config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#babel = Babel()
#key_func tulisi token
#limiter = Limiter(key_func=get_remote_address)


def create_app(configName = 'development'):
    """
    Application factory for easy configuration usage

    """
    app = Flask(__name__)
    app.config.from_object(config[configName])
    
    api = Api(app)

    #limiter.init_app(app)
    #babel.init_app(app,default_locale='en')
    #app.config['LANGUAGES'] = ['en', 'fi']

    db.init_app(app)

    from app.resources.chat import ChatLists, Chat
    api.add_resource(ChatLists, '/chats/<string:userId>')
    api.add_resource(Chat, '/chat/<string:chatId>')

    app.register_error_handler(400, bad_request)

    return app