from sqlalchemy.exc import IntegrityError

from db import db

class Participants(db.Model):
    """
    Participants class for creating 'participants' table in the database
    which contains chat participants
    """
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    chatId = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    userId = db.Column(db.String(50), nullable=False)

    def __init__(self, chatId, userId):
        self.chatId = chatId
        self.userId = userId
        self.add_to_db()

    def add_to_db(self):
        """
        Add to database       
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def serialize(self):
        return {
            'user' : self.userId
        }