import os
import uuid
from app import db
import datetime


class Chats(db.Model):
    """
    Chats class for creating 'chats' table in the database
    which includes the all the chats
    """
    __tablename__ = 'Chats'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.String(80), unique=True)
    sender_id = db.Column(db.String(80), nullable=False)
    sender2_id = db.Column(db.String(80), nullable=False)
    course_space = db.Column(db.String(80))
    messages = db.relationship('Messages', backref='chats', lazy='dynamic', order_by='Messages.timestamp')

    def __init__(self, sender_id, sender2_id, course_space):
        self.sender_id = sender_id
        self.sender2_id = sender2_id
        self.course_space = course_space
        self.chat_id = self._get_chat_id()
        #Creates new chat if not already created
        if self.chat_id == False:
            self.chat_id = self._generate_chat_id()
            self.create_chat()

    def get_chats(user):
        """
        Return all user chats
        """
        query = Chats.query.filter((Chats.sender_id == user) | (Chats.sender2_id == user)).all()
        return [chat.serialize for chat in query]
    
    def _get_chat_id(self):

        chat_id = False
    
        query = Chats.query.filter((Chats.sender_id == self.sender_id) & (Chats.sender2_id == self.sender2_id)
                            | (Chats.sender_id == self.sender2_id) & (Chats.sender2_id == self.sender_id)).all()
        
        if len(query) > 0:
            for chat in query:
                chat_id = chat.chat_id
        return chat_id
    
    def _generate_chat_id(self):
            all_chats = [chat.chat_id for chat in Chats.query.all()]
            while True:
                chat_id = uuid.uuid4()
                if chat_id not in all_chats:
                    return chat_id
    
    def create_chat(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        """
        Return object data in serializeable format
        """
        return {
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'sender2_id': self.sender2_id,
            #'messages': [Messages.serialize for message in self.messages]
        }
        


class Messages(db.Model):
    """
    Messages class for creating 'messages' table in the database
    which contains all the messages sent
    """
    __tablename__ = 'Messages'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.String(80), db.ForeignKey('Chats.chat_id'), nullable=False)
    sender = db.Column(db.String(80), nullable=False)
    #receiver = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, chat_id, sender, message):
        
        self.chat_id = chat_id
        self.sender = sender
        self.message = message
        self.create_message()

    def get_messages(chat_id):
        """
        Returns messages for specific chat
        """
        query = Messages.query.filter_by(chat_id = chat_id).order_by(Messages.timestamp.desc()).all()
        return [msg.serialize for msg in query]
    
    def create_message(self):
        """
        Add message to database       
        """
        db.session.add(self)
        db.session.commit()

    def mark_as_read(chat_id, sender):
        query = Messages.query.filter_by(chat_id = chat_id).all()

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
            'sender': self.sender,
            'message': self.message,
            'is_read': self.is_read,
            'timestamp': self.timestamp
        }