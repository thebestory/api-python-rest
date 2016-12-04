"""
The Bestory Project
"""

from thebestory.app import controllers
from thebestory.app.controllers import api


ROUTES = [
    # USERS
    {   # username can contains lowercase and uppercase letters and digits
        "path": "/users/{username:[a-zA-Z0-9]+",
        "controller": api.users.UserController
    },

    # TOPICS
    {
        "path": "/topics",
        "controller": api.topics.ColletionController
    },
    {  # topic slug can contains only lowercase letters
        "path": "/topics/{slug:[a-z]+}",
        "controller": api.topics.TopicController
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
        "controller": api.topics.HotController
    },
    {
        "path": "/topics/{slug:[a-z]+}/random",
        "controller": api.topics.RandomController
    },

    # COMMENTS
    {
        "path": "/comments",
        "controller": api.comments.ColletionController
    },
    {   # comment id can contains lowercase letters and digits
        "path": "/comments/{id:[a-z0-9]+}",
        "controller": api.comments.CommentController
    },
    {
        "path": "/comments/{id:[a-z0-9]+}/like",
        "controller": api.comments.LikeController
    },

    # STORIES

    # these routes is needed for backward compatibility
    {
        "method": "GET",
        "path": "/stories/latest",
        "controller": api.stories.BackwardCompatibilityController,
        "action": "latest",
    },
    {
        "method": "GET",
        "path": "/stories/hot",
        "controller": api.stories.BackwardCompatibilityController,
        "action": "hot",
    },
    {
        "method": "GET",
        "path": "/stories/top",
        "controller": api.stories.BackwardCompatibilityController,
        "action": "top",
    },
    {
        "method": "GET",
        "path": "/stories/random",
        "controller": api.stories.BackwardCompatibilityController,
        "action": "random",
    },

    {
        "path": "/stories",
        "controller": api.stories.CollectionController
    },
    {   # story id can contains lowercase letters and digits
        "path": "/stories/{id:[a-z0-9]+}",
        "controller": api.stories.StoryController
    },
    {
        "path": "/stories/{id:[a-z0-9]+}/like",
        "controller": api.stories.LikeController
    },
    {
        "path": "/stories/{id:[a-z0-9]+}",
        "controller": api.stories.CommentsController
    },
]
