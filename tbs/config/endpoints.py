"""
The Bestory Project
"""

# username can contains lowercase and uppercase letters, digits,
# underscore and dash
users = [
    {
        'path': '/users',
        'handler': 'users.create',
        'methods': ['POST']
    },
    {
        'path': '/users/<username:[a-zA-Z0-9_-]+>',
        'handler': 'users.show',
        'methods': ['GET']
    },
    {
        'path': '/users/<username:[a-zA-Z0-9_-]+>',
        'handler': 'users.update',
        'methods': ['PATCH', 'PUT']
    },
]

sessions = [
    {
        'path': '/sessions',
        'handler': 'sessions.index',
        'methods': ['GET']
    },
    {
        'path': '/sessions',
        'handler': 'sessions.create',
        'methods': ['POST']
    },
    {
        'path': '/sessions/<id:int>',
        'handler': 'sessions.show',
        'methods': ['GET']
    },
    {
        'path': '/sessions',
        'handler': 'sessions.delete',  # yes, we can delete only one session, now, not a bug, a feature
        'methods': ['DELETE']
    },
]

# topic slug can contains only lowercase letters
topics = [
    {
        'path': '/topics',
        'handler': 'topics.index',
        'methods': ['GET']
    },
    {
        'path': '/topics',
        'handler': 'topics.create',
        'methods': ['POST']
    },
    {
        'path': '/topics/<slug:[a-z]+>',
        'handler': 'topics.show',
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>',
        'handler': 'topics.update',
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/topics/<slug:[a-z]+>',
        'handler': 'topics.delete',
        'methods': ['DELETE']
    },

    # stories
    {
        'path': '/topics/<slug:[a-z]+>/latest',
        'handler': 'topics.lists.latest',
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>/hot',
        'handler': 'topics.lists.hot',
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>/top',
        'handler': 'topics.lists.top',
        'methods': ['GET']
    },
    {
        'path': '/topics/<slug:[a-z]+>/random',
        'handler': 'topics.lists.random',
        'methods': ['GET']
    },
]

stories = [
    {
        'path': '/stories',
        'handler': 'stories.create',
        'methods': ['POST']
    },
    {
        'path': '/stories/<id:int>',
        'handler': 'stories.show',
        'methods': ['GET']
    },
    {
        'path': '/stories/<id:int>',
        'handler': 'stories.update',
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/stories/<id:int>',
        'handler': 'stories.delete',
        'methods': ['DELETE']
    },

    # story comments
    {
        'path': '/stories/<story_id:int>/comments',
        'handler': 'stories.comments.index',
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/comments',
        'handler': 'stories.comments.create',
        'methods': ['POST']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': 'stories.comments.show',
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': 'stories.comments.create',
        'methods': ['POST']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': 'stories.comments.update',
        'methods': ['PATCH', 'PUT']
    },
    {
        'path': '/stories/<story_id:int>/comments/<id:int>',
        'handler': 'stories.comments.delete',
        'methods': ['DELETE']
    },

    # story likes
    {
        'path': '/stories/<story_id:int>/likes',
        'handler': 'stories.likes.show',
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/likes',
        'handler': 'stories.likes.create',
        'methods': ['POST', 'PATCH', 'PUT']
    },
    {
        'path': '/stories/<story_id:int>/likes',
        'handler': 'stories.likes.delete',
        'methods': ['DELETE']
    },

    # story comment likes
    {
        'path': '/stories/<story_id:int>/comments/<comment_id:int>/likes',
        'handler': 'stories.comments.likes.show',
        'methods': ['GET']
    },
    {
        'path': '/stories/<story_id:int>/comments/<comment_id:int>/likes',
        'handler': 'stories.comments.likes.create',
        'methods': ['POST', 'PATCH', 'PUT']
    },
    {
        'path': '/stories/<story_id:int>/comments/<comment_id:int>/likes',
        'handler': 'stories.comments.likes.delete',
        'methods': ['DELETE']
    },
]

root = users + sessions + topics + stories
