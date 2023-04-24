from flask import Flask
from flask_restful import Api
from app.utils.errors import bad_request
from .config import config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(configName):
    """
    Application factory for easy configuration usage

    """
    app = Flask(__name__)
    app.config.from_object(config[configName])

    api = Api(app)

    db.init_app(app)

    from app.resources.chat import ChatLists, Chat
    api.add_resource(ChatLists, '/chats/<string:userId>')
    api.add_resource(Chat, '/chat/<string:chatId>')

    app.register_error_handler(400, bad_request)

    return app