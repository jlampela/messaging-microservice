from flask import Flask, Blueprint
from flask_restful import Resource, Api
from utils.errors import bad_request


from config import config

app = Flask(__name__)
app.config.from_object(config["development"])


api = Api(app)
bp = Blueprint("api", __name__, url_prefix="/api")

    
@app.before_first_request
def create_db_tables():
    from db import db
    db.init_app(app)
    #db.drop_all()
    with app.app_context():
        db.create_all()


from resources.chat import ChatLists, Chat
api.add_resource(ChatLists, '/chat')
api.add_resource(Chat, '/chat/<string:chat_id>')

app.register_error_handler(400, bad_request)

@bp.route("/")
def index():
    return {'Status' : 'OK'}

if __name__ == '__main__':
    app.run(debug=True)
