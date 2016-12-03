"""
The Bestory Project
"""

from thebestory.app import controllers
from thebestory.app.controllers import api


ROUTES = [
    # USERS
    {
        "method": "GET",
        "path": "/users/{id:[a-zA-Z0-9]+}",
        "controller": api.users.UsersController,
        "action": "details",
    },

    # COMMENTS
    {  # comment details
        "method": "GET",
        "path": "/comments/{id:[a-z0-9]+}",
        "controller": api.comments.CommentsController,
        "action": "details",
    },
    {  # like comment
        "method": "POST",
        "path": "/comments/{id:[a-z0-9]+}/like",
        "controller": api.comments.CommentsController,
        "action": "like"
    },
    {  # unlike comment
        "method": "POST",
        "path": "/comments/{id:[a-z0-9]+}/unlike",
        "controller": api.comments.CommentsController,
        "action": "unlike"
    },
    {  # submit comment
        "method": "POST",
        "path": "/comments",
        "controller": api.comments.CommentsController,
        "action": "submit",
    },

    # STORIES
    {  # latest stories
        "method": "GET",
        "path": "/stories/latest",
        "controller": api.stories.StoriesController,
        "action": "latest",
    },
    {  # hot stories
        "method": "GET",
        "path": "/stories/hot",
        "controller": api.stories.StoriesController,
        "action": "hot",
    },
    {  # top stories
        "method": "GET",
        "path": "/stories/top",
        "controller": api.stories.StoriesController,
        "action": "top",
    },
    {  # random stories
        "method": "GET",
        "path": "/stories/random",
        "controller": api.stories.StoriesController,
        "action": "random",
    },
    {  # story details
        "method": "GET",
        "path": "/stories/{id:[a-z0-9]+}",
        "controller": api.stories.StoriesController,
        "action": "details"
    },
    {  # like story
        "method": "POST",
        "path": "/stories/{id:[a-z0-9]+}/like",
        "controller": api.stories.StoriesController,
        "action": "like"
    },
    {  # unlike story
        "method": "POST",
        "path": "/stories/{id:[a-z0-9]+}/unlike",
        "controller": api.stories.StoriesController,
        "action": "unlike"
    },
    {  # story comments
        "method": "GET",
        "path": "/stories/{id:[a-z0-9]+}/comments",
        "controller": api.stories.StoriesController,
        "action": "comments"
    },
    {  # submit story
        "method": "POST",
        "path": "/stories",
        "controller": api.stories.StoriesController,
        "action": "submit",
    },

    # TOPICS
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
