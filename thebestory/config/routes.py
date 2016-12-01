"""
The Bestory Project
"""

from thebestory.app import controllers
from thebestory.app.controllers import api


ROUTES = [
    {
        "method": "GET",
        "path": "/users/{id:[a-zA-Z0-9]+}",
        "controller": api.users.UsersController,
        "action": "details",
    },

    {
        "method": "GET",
        "path": "/comments/{id:[a-z0-9]+}",
        "controller": api.comments.CommentsController,
        "action": "details",
    },
    {
        "method": "POST",
        "path": "/comments",
        "controller": api.comments.CommentsController,
        "action": "submit",
    },

    {
        "method": "GET",
        "path": "/stories/latest",
        "controller": api.stories.StoriesController,
        "action": "latest",
    },
    {
        "method": "GET",
        "path": "/stories/hot",
        "controller": api.stories.StoriesController,
        "action": "hot",
    },
    {
        "method": "GET",
        "path": "/stories/top",
        "controller": api.stories.StoriesController,
        "action": "top",
    },
    {
        "method": "GET",
        "path": "/stories/random",
        "controller": api.stories.StoriesController,
        "action": "random",
    },
    {
        "method": "GET",
        "path": "/stories/{id:[a-z0-9]+}",
        "controller": api.stories.StoriesController,
        "action": "details"
    },
    {
        "method": "GET",
        "path": "/stories/{id:[a-z0-9]+}/comments",
        "controller": api.stories.StoriesController,
        "action": "comments"
    },
    {
        "method": "POST",
        "path": "/stories",
        "controller": api.stories.StoriesController,
        "action": "submit",
    },
    {
        "method": "GET",
        "path": "/topics",
        "controller": api.topics.TopicsController,
        "action": "list",
    },
    {
        "method": "GET",
        "path": "/topics/{id:\d+}",
        "controller": api.topics.TopicsController,
        "action": "details",
    },
    {
        "method": "GET",
        "path": "/topics/{id:\d+}/stories",
        "controller": api.topics.TopicsController,
        "action": "stories",
    },
]
