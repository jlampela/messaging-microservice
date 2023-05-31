from flask_restful import Resource, request
from flask_expects_json import expects_json
from flask import  json, make_response
#from app import limiter
#from app import babel

from app.models.chat import ChatModel
from app.models.messages import MessageModel
from app.models.participants import Participants
from app.models.schema import chat_get_schema, chat_post_schema, chatlists_get_schema, chatlists_post_schema

from app.utils.auth import user_auth
from app.utils.errors import ServiceErrors
from app.utils.helper import correct_length

class Chat(Resource):

    #Here add token authentication too
    #decorators = [limiter.limit("30/minute")]

    #@expects_json(chat_get_schema)
    def get(self, userId, chatId):
        """
        Returns specific chat based on the chat id

        Args:
            Token : Token for authorization
            userId : In the routing url
            chat_id : In the routing url      
            language : 'fi' or 'en'
        Returns:
            Messages : JSON list  

        """
        try:
            id = ChatModel.get_id(chatId)

            language = request.json['language']
            #babel.locale_selector = language

            messages = MessageModel.get_messages(id)
            if len(messages.get("messages")) < 1:
                raise ServiceErrors(404, "No chats found.")
            
            response = make_response(json.dumps(messages), 200)
            response.mimetype = "application/json"
            return response
        except ServiceErrors as e:
            return e.response

    @expects_json(chat_post_schema)
    def post(self, userId, chatId):
        """
        Sending message to specific chat

        Args:
            Token : Token for authorization
            chat_id : In the routing url      
            message (str) : text inside the request body
            msg_link (str) : Optional
            language : 'fi' or 'en'
        Returns:
            Status 

        """
        try:
            id = ChatModel.get_id(chatId)
            message = request.json["message"]
            msg_link = request.json["linked_to"]

            language = request.json['language']
            MessageModel(id, userId, correct_length(message), msg_link)

            response = make_response({'message' : 'Resource created successfully.'}, 201)
            return response
        except ServiceErrors as e:
            return e.response
        
    def put(self,userId, chatId):
        """
        Marking messages as read

        Args:
            Token : Token for authorization
            chatId : In the routing url
            UserId : Text inside the request body
        Returns:
            Status
        """
        try:
            id = ChatModel.get_id(chatId)
            a = MessageModel.mark_as_read(id, userId)
            if a is False:
                raise ServiceErrors(404, "No messages found.")
            
            response = make_response({'message' : 'Resource updated successfully.'}, 200)
            return response
        except ServiceErrors as e:
            return e.response


class ChatLists(Resource):

    #decorators = [limiter.limit("30/minute")]

    #@expects_json(chatlists_get_schema)
    def get(self, userId):
        """
        Returns all chats as a list in a way that the chat with the
        newest message comes first. Also it includes the information
        if the chat has messages you do not have read.

        Args:
            Token : Token for authorization
            user_id : Id from URL
            language : 'fi' or 'en'
        Returns:
            All the chats in JSON

        """
        try:
            chat_list = ChatModel.get_chats(userId)
            language = request.json['language']
            
            if len(chat_list) < 1:
                raise ServiceErrors(404, "No chats found.")

            response = make_response(json.dumps(chat_list), 200)
            response.mimetype = "application/json"
            return response
        except ServiceErrors as e:
            return e.response

    @expects_json(chatlists_post_schema)
    def post(self, userId):
        """
        Creates a new chat 1-on-1 with a user or a group chat

        Args:
            userId (str) : text inside the url
            Receiver (str) OR (list) : text inside the request body
            Course_space (str) : text inside the request body
            Topic (str) : text inside the request body
            Message (str) : text inside the request body        
            language : 'fi' or 'en'
        Returns:
            Status (Key-Value pair) : text in JSON    

        """
        try:
            chat_id = None

            receiver = request.json["receiver"]
            course_space = request.json["course_space"]
            topic = request.json["topic"]
            message = request.json["message"]
            language = request.json['language']

            if isinstance(receiver, list):
                #Creates group chat
                group_chat = ChatModel(course_space, topic, "Group", language)
                
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
                private_chat = ChatModel(course_space, topic, "Private", language)

                #Add participants to db
                sender = Participants(private_chat.id, userId)
                receive = Participants(private_chat.id, receiver)

                #Now creates the message that is linked to the chat
                MessageModel(private_chat.id, userId, correct_length(message))
                chat_id = private_chat.chat_id

            response = make_response({'message' : 'Resource created successfully.'}, 201)
            response.headers['Location'] = f"/chat/{chat_id}"
            return response
        except ServiceErrors as e:
            return e.response