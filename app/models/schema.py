
chat_get_schema = {
    'type' : 'object',
    'properties' : {
        'language' : {'type' : 'string'}
    },
    'required' : ['sender', 'language']
}

chat_post_schema = {
    'type' : 'object',
    'properties' : {
        'message' : {'type' : 'string'},
        'linked_to' : {'type' : 'string'},
        'language' : {'type' : 'string'}
    },
    'required' : ['message', 'language']
}

chatlists_get_schema = {
    'type' : 'object',
    'properties' : {
        'language' : {'type' : 'string'}
    },
    'required' : ['language']
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

