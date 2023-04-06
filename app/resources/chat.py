from flask_restful import Resource, request
from flask_expects_json import expects_json
from flask import  json, make_response

from models.chat import ChatModel
from models.messages import MessageModel
from models.participants import Participants
from models.schema import chat_get_schema, chat_post_schema, chatlists_get_schema, chatlists_post_schema

from utils.auth import user_auth
from utils.errors import ServiceErrors
from utils.helper import correct_length

class Chat(Resource):

    #id = request.headers.get('Token')

    #@user_auth(2)
    #@expects_json(chat_get_schema)
    def get(self, userId, chatId):
        """
        Returns specific chat based on the chat id

        Args:
            Token : Token for authorization
            chat_id : In the routing url      

        Returns:
            Messages : JSON list  

        """
        try:
            chat = ChatModel.
            #MessageModel.mark_as_read(chatId, userId)
            #messages = MessageModel.get_messages(chatId)
            if len(messages) < 1:
                raise ServiceErrors(403, "No chats found.")
            
            response = make_response(json.dumps(messages), 200)
            response.mimetype = "application/json"
            return response
        except ServiceErrors as e:
            return e.response

    #@user_auth(id)
    #@expects_json(chat_post_schema)
    def post(self, userId, chatId):
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
            message = request.json["message"]
            msg_link = request.json["linked_to"]
            MessageModel(chatId, userId, correct_length(message), msg_link)

            response = make_response({'message' : 'Resource created successfully'}, 201)
            return response
        except ServiceErrors as e:
            return e.response

class ChatLists(Resource):

    #@user_auth(id)
    #@expects_json(chatlists_get_schema)
    def get(self, userId):
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
            chat_list = ChatModel.get_chats(userId)
            if len(chat_list) < 1:
                raise ServiceErrors(404, "No chats found.")

            response = make_response(json.dumps(chat_list), 200)
            response.mimetype = "application/json"
            return response
        except ServiceErrors as e:
            return e.response

    #@user_auth(id)
    #fixaa schemat
    #@expects_json(chatlists_post_schema)
    def post(self, userId):
        """
        Creates a new chat 1-on-1 with a user or a group chat

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
            chat_id = None

            receiver = request.json["receiver"]
            course_space = request.json["course_space"]
            topic = request.json["topic"]
            message = request.json["message"]

            if isinstance(receiver, list):
                #Creates group chat
                group_chat = ChatModel(course_space, topic, "Group")
                
                #Add the sender
                Participants(group_chat.id, userId)
                #Add participants to db
                for participant in receiver:
                    Participants(group_chat.id, participant)

                #Now creates the message that is linked to the chat
                MessageModel(group_chat.id, userId, correct_length(message))
                chat_id = group_chat.chat_id
            else:
                #Creates private chat
                private_chat = ChatModel(course_space, topic, "Private")

                #Add participants to db
                sender = Participants(private_chat.id, userId)
                receiver = Participants(private_chat.id, receiver)

                #Now creates the message that is linked to the chat
                MessageModel(private_chat.id, userId, correct_length(message))
                chat_id = private_chat.chat_id

            response = make_response({'message' : 'Resource created successfully'}, 201)
            response.headers['Location'] = f"/chat/{chat_id}"
            return response
        except ServiceErrors as e:
            return e.response