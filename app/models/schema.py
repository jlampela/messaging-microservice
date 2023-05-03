
chat_get_schema = {
    'type' : 'object',
    'properties' : {
        'sender' : {'type' : 'string'},
        'language' : {'type' : 'string'}
    },
    'required' : ['sender', 'language']
}

chat_post_schema = {
    'type' : 'object',
    'properties' : {
        'userId' : {'type' : 'string'},
        'message' : {'type' : 'string'},
        'linked_to' : {'type' : 'string'},
        'language' : {'type' : 'string'}
    },
    'required' : ['userId', 'message', 'language']
}

chatlists_get_schema = {
    'type' : 'object',
    'properties' : {
        'sender' : {'type' : 'string'},
        'language' : {'type' : 'string'}
    },
    'required' : ['sender', 'language']
}

chatlists_post_schema = {
    'type' : 'object',
    'properties' : {
        'receiver' : {'type' : ['string', 'array']},
        'course_space' : {'type' : 'string'},
        'topic' : {'type' : 'string'},
        'message' : {'type' : 'string'},
        'language' : {'type' : 'string'}
    },
    'required' : ['receiver', 'course_space', 'topic', 'message', 'language']
}