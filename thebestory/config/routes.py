"""
The Bestory Project
"""

from thebestory.app import controllers
from thebestory.app.controllers import api


ROUTES = [
    {
        "method": "GET",
        "path": "/api/users/{id:\d+}",
        "controller": api.users.UsersController,
        "action": "details",
    },

    {
        "method": "GET",
        "path": "/api/comments/{id:\d+}",
        "controller": api.comments.CommentsController,
        "action": "details",
    },
    {
        "method": "POST",
        "path": "/api/comments",
        "controller": api.comments.CommentsController,
        "action": "submit",
    },

    {
        "method": "GET",
        "path": "/api/stories/{id:\d+}",
        "controller": api.stories.StoriesController,
        "action": "details"
    },
    {
        "method": "GET",
        "path": "/api/stories/latest",
        "controller": api.stories.StoriesController,
        "action": "latest",
    },
    {
        "method": "GET",
        "path": "/api/stories/hot",
        "controller": api.stories.StoriesController,
        "action": "hot",
    },
    {
        "method": "GET",
        "path": "/api/stories/top",
        "controller": api.stories.StoriesController,
        "action": "top",
    },
    {
        "method": "GET",
        "path": "/api/stories/random",
        "controller": api.stories.StoriesController,
        "action": "random",
    },
    {
        "method": "POST",
        "path": "/api/stories",
        "controller": api.stories.StoriesController,
        "action": "submit",
    },

    {
        "method": "GET",
        "path": "/api/topics",
        "controller": api.topics.TopicsController,
        "action": "list",
    },
    {
        "method": "GET",
        "path": "/api/topics/{id:\d+}",
        "controller": api.topics.TopicsController,
        "action": "details",
    },
    {
        "method": "GET",
        "path": "/api/topics/{id:\d+}/stories",
        "controller": api.topics.TopicsController,
        "action": "stories",
    },
]
