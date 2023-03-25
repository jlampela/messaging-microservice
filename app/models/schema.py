
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
        'sender' : {'type' : 'string'},
        'message' : {'type' : 'string'},
        'linked_to' : {'type' : 'string'}
    },
    'required' : ['sender', 'message']
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
        'sender' : {'type' : 'string'},
        'receiver' : {'type' : 'string'},
        'course_space' : {'type' : 'string'},
        'topic' : {'type' : 'string'},
        'message' : {'type' : 'string'},
    },
    'required' : ['sender', 'receiver', 'course_space', 'topic', 'message',]
}