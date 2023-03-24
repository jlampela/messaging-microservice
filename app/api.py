from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import config

app = Flask(__name__)
app.config.from_object(config["development"])

db = SQLAlchemy()
api = Api(app)
bp = Blueprint("api", __name__, url_prefix="/api")

    
@app.before_first_request
def create_db_tables():
    db.init_app(app)
    with app.app_context():
        db.create_all()


from resources.chat import ChatLists, Chat
api.add_resource(ChatLists, '/chat')
api.add_resource(Chat, '/chat/<string:name>')

@bp.route("/")
def index():
    return {'Status' : 'OK'}

if __name__ == '__main__':
    app.run(debug=True)
