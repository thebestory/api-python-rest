"""
The Bestory Project
"""

from thebestory.config import app
from thebestory.config import db
from thebestory.controllers import api


mw = []

routes = [
    # USERS
    {  # username can contains lowercase and uppercase letters and digits
        "path": "/users/{username:[a-zA-Z0-9]+}",
        "controller": api.users.UserController
    },

    # TOPICS
    {
        "path": "/topics",
        "controller": api.topics.CollectionController
    },
    {  # topic slug can contains only lowercase letters
        "path": "/topics/{slug:[a-z]+}",
        "controller": api.topics.TopicController
    },
    {
        "path": "/topics/{slug:[a-z]+}/unapproved",
        "controller": api.topics.UnapprovedController
    },
    {
        "path": "/topics/{slug:[a-z]+}/latest",
        "controller": api.topics.LatestController
    },
    {
        "path": "/topics/{slug:[a-z]+}/hot",
        "controller": api.topics.HotController
    },
    {
        "path": "/topics/{slug:[a-z]+}/top",
        "controller": api.topics.TopController
    },
    {
        "path": "/topics/{slug:[a-z]+}/random",
        "controller": api.topics.RandomController
    },

    # COMMENTS
    {
        "path": "/comments",
        "controller": api.comments.CollectionController
    },
    {  # comment id can contains lowercase letters and digits
        "path": "/comments/{id:[a-z0-9]+}",
        "controller": api.comments.CommentController
    },
    {
        "path": "/comments/{id:[a-z0-9]+}/like",
        "controller": api.comments.LikeController
    },

    # STORIES
    {
        "path": "/stories",
        "controller": api.stories.CollectionController
    },
    {  # story id can contains lowercase letters and digits
        "path": "/stories/{id:[a-z0-9]+}",
        "controller": api.stories.StoryController
    },
    {
        "path": "/stories/{id:[a-z0-9]+}/like",
        "controller": api.stories.LikeController
    },
    {
        "path": "/stories/{id:[a-z0-9]+}/comments",
        "controller": api.stories.CommentsController
    },
]
