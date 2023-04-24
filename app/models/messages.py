from sqlalchemy import and_, null
from sqlalchemy.exc import IntegrityError
from app import db
import datetime


class MessageModel(db.Model):
    """
    Messages class for creating 'messages' table in the database
    which contains all the messages sent
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    linked_to = db.Column(db.Integer, db.ForeignKey('messages.id'))

    def __init__(self, chat_id, sender, message, linked_to=None):
        self.chat_id = chat_id
        self.sender = sender
        self.message = message
        self.linked_to = linked_to
        self.create_message()

    def get_messages(chat_id):
        """
        Returns messages for specific chat
        """
        query = MessageModel.query\
            .filter(chat_id == MessageModel.chat_id)\
            .order_by(MessageModel.timestamp.desc())\
            .all()

        return {'messages' : [msg.serialize for msg in query]}
    
    def create_message(self):
        """
        Add message to database       
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def mark_as_read(chat_id, sender):
        """
        Marks the message read status
        """
        query = MessageModel.query.filter_by(chat_id = chat_id).all()

        for msg in query:
            if msg.sender != sender and msg.is_read == False:
                msg.is_read = True
        db.session.commit()

    @property
    def serialize(self):
        """
        Return object data in serializeable format
        """
        return {
            'id' : self.id,
            'sender': self.sender,
            'message': self.message,
            'is_read': self.is_read,
            'timestamp': self.timestamp,
            'linked_to' : self.linked_to
        }