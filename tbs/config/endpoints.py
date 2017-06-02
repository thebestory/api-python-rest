"""
The Bestory Project
"""

from tbs.controllers import sessions as sessions_controller
from tbs.controllers import stories as stories_controller
from tbs.controllers import topics as topics_controller
from tbs.controllers import users as users_controller


users = [
    {
        "path": "/users",
        "handler": users_controller.create_user,
        "methods": ["POST"]
    },
    {
        "path": "/users/<id:int>",
        "handler": users_controller.show_user,
        "methods": ["GET"]
    },
    {
        "path": "/users/<id:int>",
        "handler": users_controller.update_user,
        "methods": ["PATCH", "PUT"]
    },
]

sessions = [
    {
        "path": "/sessions",
        "handler": sessions_controller.list_sessions,
        "methods": ["GET"]
    },
    {
        "path": "/sessions",
        "handler": sessions_controller.create_session,
        "methods": ["POST"]
    },
    {
        "path": "/sessions",
        "handler": sessions_controller.delete_session,  # delete current session
        "methods": ["DELETE"]
    },
    {
        "path": "/sessions/<id:int>",
        "handler": sessions_controller.show_session,
        "methods": ["GET"]
    },
    {
        "path": "/sessions/<id:int>",
        "handler": sessions_controller.delete_session,
        "methods": ["DELETE"]
    }
]

topics = [
    {
        "path": "/topics",
        "handler": topics_controller.list_topics,
        "methods": ["GET"]
    },
    {
        "path": "/topics",
        "handler": topics_controller.create_topic,
        "methods": ["POST"]
    },
    {
        "path": "/topics/<id:int>",
        "handler": topics_controller.show_topic,
        "methods": ["GET"]
    },
    {
        "path": "/topics/<id:int>",
        "handler": topics_controller.update_topic,
        "methods": ["PATCH", "PUT"]
    },
    {
        "path": "/topics/<id:int>",
        "handler": topics_controller.delete_topic,
        "methods": ["DELETE"]
    },

    # stories
    {
        "path": "/topics/<id:int>/latest",
        "handler": topics_controller.list_topic_latest_stories,
        "methods": ["GET"]
    },
    {
        "path": "/topics/<id:int>/hot",
        "handler": topics_controller.list_topic_hot_stories,
        "methods": ["GET"]
    },
    {
        "path": "/topics/<id:int>/top",
        "handler": topics_controller.list_topic_top_stories,
        "methods": ["GET"]
    },
    {
        "path": "/topics/<id:int>/random",
        "handler": topics_controller.list_topic_random_stories,
        "methods": ["GET"]
    },
]

stories = [
    {
        "path": "/stories",
        "handler": stories_controller.create_story,
        "methods": ["POST"]
    },
    {
        "path": "/stories/<id:int>",
        "handler": stories_controller.show_story,
        "methods": ["GET"]
    },
    {
        "path": "/stories/<id:int>",
        "handler": stories_controller.update_story,
        "methods": ["PATCH", "PUT"]
    },
    {
        "path": "/stories/<id:int>",
        "handler": stories_controller.delete_story,
        "methods": ["DELETE"]
    },

    # story reactions
    {
        "path": "/stories/<story_id:int>/likes",
        "handler": stories_controller.list_story_reactions,
        "methods": ["GET"]
    },
    {
        "path": "/stories/<story_id:int>/likes",
        "handler": stories_controller.create_story_reaction,
        "methods": ["POST", "PATCH", "PUT"]
    },
    {
        "path": "/stories/<story_id:int>/likes",
        "handler": stories_controller.delete_story_reaction,
        "methods": ["DELETE"]
    },

    # story comments
    {
        "path": "/stories/<story_id:int>/comments",
        "handler": stories_controller.list_story_comments,
        "methods": ["GET"]
    },
    {
        "path": "/stories/<story_id:int>/comments",
        "handler": stories_controller.create_story_comment,
        "methods": ["POST"]
    },
    {
        "path": "/stories/<story_id:int>/comments/<id:int>",
        "handler": stories_controller.show_story_comment,
        "methods": ["GET"]
    },
    {
        "path": "/stories/<story_id:int>/comments/<id:int>",
        "handler": stories_controller.update_story_comment,
        "methods": ["PATCH", "PUT"]
    },
    {
        "path": "/stories/<story_id:int>/comments/<id:int>",
        "handler": stories_controller.delete_story_comment,
        "methods": ["DELETE"]
    },

    # story comment reactions
    {
        "path": "/stories/<story_id:int>/comments/<comment_id:int>/likes",
        "handler": stories_controller.list_story_comment_reactions,
        "methods": ["GET"]
    },
    {
        "path": "/stories/<story_id:int>/comments/<comment_id:int>/likes",
        "handler": stories_controller.create_story_comment_reaction,
        "methods": ["POST", "PATCH", "PUT"]
    },
    {
        "path": "/stories/<story_id:int>/comments/<comment_id:int>/likes",
        "handler": stories_controller.delete_story_comment_reaction,
        "methods": ["DELETE"]
    },
]

root = users + sessions + topics + stories
