from flask import Blueprint, jsonify, request
from app.models import Chats, Messages
from app.utils.auth import user_auth
from app.utils.errors import (
    ServiceErrors,
    unauthorized
)

chats = Blueprint('chats', __name__)

@chats.route('/')
def status():
    Chats("12","13","testi")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "12", "asd")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "13", "ads")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "12", "ads")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "13", "cs")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "12", "sd")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "13", "as")
    Messages("5f242e8a-1bd0-4a44-97e2-6e64aba202bf", "12", "aa")
    return jsonify({'status': 'ok'})

@chats.route('/chats', methods=['GET'])
def return_all_chats():
    """
    Returns all chats as a list

    Args:
        Token : Token for authorization
        Sender (str) : text inside the request body

    Returns:
        All the chats in JSON

    """
    try:
        id = request.args.get('Token')
        if not user_auth(id):
            return unauthorized("Authorization failed")
        sender = request.form.get('sender')
        return jsonify(Chats.get_chats(sender))
    except Exception as er:
        raise ServiceErrors(er.code, er.message)

@chats.route('/chats', methods=['POST'])
def create_chat():
    """
    Creates a new chat with a user

    Args:
        Token : Token for authorization
        Sender (str) : text inside the request body
        Receiver (str) : text inside the request body
        Course_space (str) : text inside the request body
        Message (str) : text inside the request body        

    Returns:
        Status (Key-Value pair) : text in JSON    

    """
    try:
        #pitäisikö tällä tokenilla haettaessa palauttaa esim username?
        id = request.args.get('Token') 
        if not user_auth(id): #muokkaa että laittaa exceptionin
            return unauthorized("Authorization failed")
        
        sender = request.form.get('sender') #sender_id
        receiver = request.form.get('receiver') #sender2_id
        course_space = request.form.get('course_space')

        #Creates the chat
        new_chat = Chats(sender, receiver, course_space)

        #Now creates the message that is linked to the chat
        message = request.form.get('message')
        Messages(new_chat.chat_id, id, message)

    except Exception as er:
        raise ServiceErrors(er.code, er.message)

    return jsonify({'status': 'ok'})


@chats.route('/chats/<chat_id>', methods=['GET'])
def return_chat(chat_id):
    """
    Returns specific chat based on the chat id

    Args:
        Token : Token for authorization
        chat_id : In the routing url      

    Returns:
        Messages : JSON list  


    """
    
    try:
        id = request.args.get('Token') 
        if not user_auth(id):
            return unauthorized("Authorization failed")
        return jsonify(Messages.get_messages(chat_id))
    except Exception as er:
        raise ServiceErrors(er.code, er.message)


@chats.route('/chats/<chat_id>/read', methods=['PUT'])
def mark_as_read(chat_id):
    """
    Marks messages as read

    Args:
        Token : Token for authorization
        Sender (str) : text inside the request body      

    Returns:
        Status (Key-Value pair) : text in JSON    

    """
    try:
        id = request.args.get('Token') 
        if not user_auth(id):
            return unauthorized("Authorization failed")
        sender = request.form.get('sender')
        Messages.mark_as_read(chat_id, sender)
        return jsonify({'status': 'ok'})
    except Exception as er:
        raise ServiceErrors(er.code, er.message)