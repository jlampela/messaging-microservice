
chat_get_schema = {
    'type' : 'object',
    'properties' : {
        'sender' : {'type' : 'string'}
    },
    'required' : ['sender']
}

chat_post_schema = {
    'type' : 'object',
    'properties' : {
        'userId' : {'type' : 'string'},
        'message' : {'type' : 'string'},
        'linked_to' : {'type' : 'string'}
    },
    'required' : ['userId', 'message']
}

chatlists_get_schema = {
    'type' : 'object',
    'properties' : {
        'sender' : {'type' : 'string'},
    },
    'required' : ['sender']
}

chatlists_post_schema = {
    'type' : 'object',
    'properties' : {
        'receiver' : {'type' : ['string', 'array']},
        'course_space' : {'type' : 'string'},
        'topic' : {'type' : 'string'},
        'message' : {'type' : 'string'},
    },
    'required' : ['receiver', 'course_space', 'topic', 'message',]
}