from app import create_app
from app.models import Chats, Messages

app = create_app("development")

if __name__ == '__main__':
    app.run()