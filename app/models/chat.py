from uuid import uuid4

from models.messages import MessageModel
from models.participants import Participants

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from db import db


class ChatModel(db.Model):
    """
    ChatModel class for creating 'chatModel' table in the database
    which includes the all the chatModel.
    """
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.String(80), unique=True)
    topic = db.Column(db.String(80), nullable=False)
    course_space = db.Column(db.String(80))
    type = db.Column(db.String(50))
    messages = db.relationship('MessageModel', backref='chats', lazy='dynamic', order_by='MessageModel.timestamp')
    participants = db.relationship('Participants', lazy='dynamic')

    def __init__(self, course_space, topic, type):
        self.course_space = course_space
        self.topic = topic
        self.type = type
        self.chat_id = uuid4()
        self.create_chat()

        #fixaa
        #self.chat_id = self._get_chat_id()
        #Creates new chat if not already created
        #if self.chat_id == False:
            #self.chat_id = self._generate_chat_id()
            #self.create_chat()

    def get_chats(userId):
        """
        FIX
        Return all user chats as a list
        """
        #query = ChatModel.query\
        #    .join(MessageModel, MessageModel.chat_id == ChatModel.chat_id)\
        #    .filter((ChatModel.sender_id == user) | (ChatModel.sender2_id == user))\
        #    .order_by(MessageModel.timestamp.desc())\
        #    .all()

        query = ChatModel.query\
            .join(Participants)\
            .join(MessageModel, ChatModel.id == MessageModel.chat_id)\
            .filter(Participants.userId == userId)\
            .order_by(MessageModel.timestamp.desc())\
            .all()

        return [chat.serialize(userId) for chat in query]

    
    def _get_chat_id(self):
        """
        FIX
        Query for chats that have been already created
        """

        chat_id = False
    
        query = ChatModel.query.filter((ChatModel.sender_id == self.sender_id) & (ChatModel.sender2_id == self.sender2_id)
                            | (ChatModel.sender_id == self.sender2_id) & (ChatModel.sender2_id == self.sender_id)).all()
        
        if len(query) > 0:
            for chat in query:
                chat_id = chat.chat_id
        return chat_id
    
    def _generate_chat_id(self):
        """
        Generate a new UUID for the chat
        """
        all_chatModel = [chat.chat_id for chat in ChatModel.query.all()]
        while True:
            chat_id = uuid4()
            if chat_id not in all_chatModel:
                return chat_id
    
    def create_chat(self):
        """
        Adds the chat to database
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def is_unread(self, user):
        """
        FIX
        Checks for unread messages
        """
        t = self.messages.filter(and_(MessageModel.is_read == False, MessageModel.sender != user)).first()
        if t is None:
            return False
        return True

    def serialize(self, user):
        """
        FIX
        Return object data in serializeable format
        """

        return {
            'chat_id': self.chat_id,
            'participants' : [x.userId for x in self.participants if x.userId != user],
            'topic': self.topic,
            'course_space' : self.course_space,
            'type' : self.type,
            'unread_msg': self.is_unread(user)
        }