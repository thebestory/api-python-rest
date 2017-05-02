"""
The Bestory Project
"""

from thebestory import controllers

# username can contains lowercase and uppercase letters, digits,
# underscore and dash
users = [
    {
        'path': '/users',
        'handler': controllers.users.create,
        'methods': ['POST']
    },
    {
        'path': '/users/<username:[a-zA-Z0-9_-]+>',
        'handler': controllers.users.show,
        'methods': ['GET']
    },
    {
        'path': '/users/<username:[a-zA-Z0-9_-]+>',
        'handler': controllers.users.update,
        'methods': ['PATCH', 'PUT']
    },
]

sessions = [
    {
        'path': '/sessions',
        'handler': controllers.sessions.index,
        'methods': ['GET']
    },
    {
        'path': '/sessions',
        'handler': controllers.sessions.create,
        'methods': ['POST']
    },
    {
        'path': '/sessions/<id:[0-9]+>',
        'handler': controllers.sessions.show,
        'methods': ['GET']
    },
    {
        'path': '/sessions',
        'handler': controllers.sessions.delete,  # yes, we can delete only one session, now, not a bug, a feature
        'methods': ['DELETE']
    },
]

# topic slug can contains only lowercase letters
topics = [
    {
        'path': '/topics',
        'handler': controllers.topics.index,
        'methods': ['GET']
    },
    {
        'path': '/topics',
        'handler': controllers.topics.create,
        'methods': ['POST']
    },
    {
        'path': '/topics/<slug:[a-z]+>',
        'handler': controllers.topics.show,
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>',
        'handler': controllers.topics.update,
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/topics/<slug:[a-z]+>',
        'handler': controllers.topics.delete,
        'methods': ['DELETE']
    },
]

comments = [
    {
        'path': '/comments/<id:[0-9]+>',
        'handler': controllers.comments.show,
        'methods': ['GET']
    },
    {
        'path': '/comments/<id:[0-9]+>',
        'handler': controllers.comments.create,
        'methods': ['POST']
    },
    {
        'path': '/comments/<id:[0-9]+>',
        'handler': controllers.comments.update,
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/comments/<id:[0-9]+>',
        'handler': controllers.comments.delete,
        'methods': ['DELETE']
    },
]

reactions = [
    {
        'path': '/reactions/<id:[0-9]+>',
        'handler': controllers.reactions.show,
        'methods': ['GET']
    },
    {
        'path': '/reactions/<id:[0-9]+>',
        'handler': controllers.reactions.create,
        'methods': ['POST', 'PATCH', 'PUT']
    },
    {
        'path': '/reactions/<id:[0-9]+>',
        'handler': controllers.reactions.delete,
        'methods': ['DELETE']
    },
]

stories = [
    {
        'path': '/stories',
        'handler': controllers.stories.create,
        'methods': ['DELETE']
    },
    {
        'path': '/stories/<id:[0-9]+>',
        'handler': controllers.stories.show,
        'methods': ['GET']
    },
    {
        'path': '/stories/<id:[0-9]+>',
        'handler': controllers.stories.update,
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/stories/<id:[0-9]+>',
        'handler': controllers.stories.delete,
        'methods': ['DELETE']
    },
]

root = users + sessions + topics + comments + reactions + stories
