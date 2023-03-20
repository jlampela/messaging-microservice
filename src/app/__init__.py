from flask import Flask
from .config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from app.chats.messaging import chats
    app.register_blueprint(chats)

    return app