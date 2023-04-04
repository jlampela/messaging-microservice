from flask import Flask, Blueprint
from flask_restful import Resource, Api
from utils.errors import bad_request


from config import config

app = Flask(__name__)
app.config.from_object(config["development"])


api = Api(app)
bp = Blueprint('api', __name__)
#app.register_blueprint(bp)
    
@app.before_first_request
def create_db_tables():
    from db import db
    db.init_app(app)
    #db.drop_all()
    with app.app_context():
        db.create_all()


from resources.chat import ChatLists, Chat
api.add_resource(ChatLists, '/chat/<string:userId>')
api.add_resource(Chat, '/chat/<string:userId>/<string:chatId>')

app.register_error_handler(400, bad_request)

@app.route("/")
def index():   
    return {'status' : 'ok'}

if __name__ == '__main__':
    app.run(debug=True)
