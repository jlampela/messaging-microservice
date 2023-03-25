from uuid import uuid4
from models.messages import MessageModel
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, NoResultFound
from db import db


class ChatModel(db.Model):
    """
    ChatModel class for creating 'chatModel' table in the database
    which includes the all the chatModel.
    """
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    chat_id = db.Column(db.String(80), unique=True)
    sender_id = db.Column(db.String(80), nullable=False)
    sender2_id = db.Column(db.String(80), nullable=False)
    topic = db.Column(db.String(80), nullable=False)
    course_space = db.Column(db.String(80))
    messages = db.relationship('MessageModel', backref='chats', lazy='dynamic', order_by='MessageModel.timestamp')

    def __init__(self, sender_id, sender2_id, course_space, topic):
        self.sender_id = sender_id
        self.sender2_id = sender2_id
        self.course_space = course_space
        self.topic = topic
        self.chat_id = self._get_chat_id()
        #Creates new chat if not already created
        if self.chat_id == False:
            self.chat_id = self._generate_chat_id()
            self.create_chat()

    def get_chats(user):
        """
        Return all user chatModel
        """
        query = ChatModel.query\
            .join(MessageModel, MessageModel.chat_id == ChatModel.chat_id)\
            .filter((ChatModel.sender_id == user) | (ChatModel.sender2_id == user))\
            .order_by(MessageModel.timestamp.desc())\
            .all()

        return [chat.serialize(user) for chat in query]

    
    def _get_chat_id(self):

        chat_id = False
    
        query = ChatModel.query.filter((ChatModel.sender_id == self.sender_id) & (ChatModel.sender2_id == self.sender2_id)
                            | (ChatModel.sender_id == self.sender2_id) & (ChatModel.sender2_id == self.sender_id)).all()
        
        if len(query) > 0:
            for chat in query:
                chat_id = chat.chat_id
        return chat_id
    
    def _generate_chat_id(self):
            all_chatModel = [chat.chat_id for chat in ChatModel.query.all()]
            while True:
                chat_id = uuid4()
                if chat_id not in all_chatModel:
                    return chat_id
    
    def create_chat(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def is_unread(self, user):
        t = self.messages.filter(and_(MessageModel.is_read == False, MessageModel.sender != user)).first()
        if t is None:
            return False
        return True

    def serialize(self, user):
        """
        Return object data in serializeable format
        """
        return {
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'sender2_id': self.sender2_id,
            'course_space' : self.course_space,
            'unread_msg': self.is_unread(user)
        }