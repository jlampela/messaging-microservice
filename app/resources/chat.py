from flask_restful import Resource, abort, request
from flask_expects_json import expects_json, ValidationError
from flask import Response, json

from utils.auth import user_auth
from models.chat import ChatModel
from models.messages import MessageModel
from models.schema import chat_get_schema, chat_post_schema, chatlists_get_schema, chatlists_post_schema
from utils.errors import ServiceErrors
from utils.helper import correct_length

class Chat(Resource):

    #id = request.headers.get('Token')

    #@user_auth(2)
    @expects_json(chat_get_schema)
    def get(self, chat_id):
        """
        Returns specific chat based on the chat id

        Args:
            Token : Token for authorization
            chat_id : In the routing url      

        Returns:
            Messages : JSON list  

        """
        try:
            sender = request.json["sender"]
            MessageModel.mark_as_read(chat_id, sender)
            messages = MessageModel.get_messages(chat_id)
            if len(messages) < 1:
                raise ServiceErrors(403, "No chats found.")
            return Response(response=json.dumps(messages),status=200, mimetype="application/json")
        except ServiceErrors as e:
            return e.response

    #@user_auth(id)
    @expects_json(chat_post_schema)
    def post(self, chat_id):
        """
        Sending message to specific chat

        Args:
            Token : Token for authorization
            chat_id : In the routing url      
            message (str) : text inside the request body
        Returns:
            Status 

        """
        try:
            sender = request.json["sender"]
            message = request.json["message"]
            msg_link = request.json["linked_to"]
            MessageModel(chat_id, sender, correct_length(message), msg_link)
            return Response(status=201)
        except ServiceErrors as e:
            return e.response

class ChatLists(Resource):

    #@user_auth(id)
    @expects_json(chatlists_get_schema)
    def get(self):
        """
        Returns all chats as a list in a way that the chat with the
        newest message comes first. Also it includes the information
        if the chat has messages you do not have read.

        Args:
            Token : Token for authorization
            Sender (str) : text inside the request body

        Returns:
            All the chats in JSON

        """
        try:
            sender = request.json["sender"]
            chat_list = ChatModel.get_chats(sender)
            if len(chat_list) < 1:
                raise ServiceErrors(404, "No chats found.")
            return Response(response=json.dumps(chat_list),status=200, mimetype="application/json")
        except ServiceErrors as e:
            return e.response

    #@user_auth(id)
    @expects_json(chatlists_post_schema)
    def post(self):
        """
        Creates a new chat with a user

        Args:
            Sender (str) : text inside the request body
            Receiver (str) : text inside the request body
            Course_space (str) : text inside the request body
            Topic (str) : text inside the request body
            Message (str) : text inside the request body        

        Returns:
            Status (Key-Value pair) : text in JSON    

        """
        try:
            sender = request.json["sender"]
            receiver = request.json["receiver"]
            course_space = request.json["course_space"]
            topic = request.json["topic"]
            message = request.json["message"]

            #Creates the chat
            new_chat = ChatModel(sender, receiver, course_space, topic)

            #Now creates the message that is linked to the chat
            MessageModel(new_chat.chat_id, sender, message)
            return Response(status=201)
        except ServiceErrors as e:
            return e.response