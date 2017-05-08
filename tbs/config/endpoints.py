"""
The Bestory Project
"""

from tbs import controllers

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
        'path': '/sessions/<id:int>',
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

    # stories
    {
        'path': '/topics/<slug:[a-z]+>/latest',
        'handler': controllers.topics.lists.latest,
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>/hot',
        'handler': controllers.topics.lists.hot,
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>/top',
        'handler': controllers.topics.lists.top,
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>/random',
        'handler': controllers.topics.lists.random,
        'methods': ['GET']
    },
]

stories = [
    {
        'path': '/stories',
        'handler': controllers.stories.create,
        'methods': ['POST']
    },
    {
        'path': '/stories/<id:int>',
        'handler': controllers.stories.show,
        'methods': ['GET']
    },
    {
        'path': '/stories/<id:int>',
        'handler': controllers.stories.update,
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/stories/<id:int>',
        'handler': controllers.stories.delete,
        'methods': ['DELETE']
    },

    # story comments
    {
        'path': '/stories/<story_id:int>/comments',
        'handler': controllers.stories.comments.index,
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/comments',
        'handler': controllers.stories.comments.create,
        'methods': ['POST']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': controllers.stories.comments.show,
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': controllers.stories.comments.create,
        'methods': ['POST']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': controllers.stories.comments.update,
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': controllers.stories.comments.delete,
        'methods': ['DELETE']
    },

    # story likes
    {
        'path': '/stories/<story_id:int>/likes',
        'handler': controllers.stories.likes.show,
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/likes',
        'handler': controllers.stories.likes.create,
        'methods': ['POST', 'PATCH', 'PUT']
    },
    {
        'path': '/stories/<story_id:int>/likes',
        'handler': controllers.stories.likes.delete,
        'methods': ['DELETE']
    },

    # story comment likes
    {
        'path': '/stories/<story_id:int>/comments/<comment_id:int>/likes',
        'handler': controllers.stories.comments.likes.show,
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/comments/<comment_id:int>/likes',
        'handler': controllers.stories.comments.likes.create,
        'methods': ['POST', 'PATCH', 'PUT']
    },
    {
        'path': '/stories/<story_id:int>/comments/<comment_id:int>/likes',
        'handler': controllers.stories.comments.likes.delete,
        'methods': ['DELETE']
    },
]

root = users + sessions + topics + stories
