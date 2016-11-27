"""
The Bestory Project
"""

from thebestory.app.lib import identifier


def story(s,
          prefix="",
          prefix_topic="topic_",
          extended=True):
    data = dict()

    data["id"] = identifier.to36(s[prefix + "id"])

    if t is not None:
        data["topic"] = topic(t, extended_t)
    else:
        data["topic"]["id"] = s[prefix + "topic_id"]

    data["content"] = s[prefix + "content"]

    data["likes_count"] = s[prefix + "likes_count"]
    data["comments_count"] = s[prefix + "comments_count"]

    data["submitted_date"] = s[prefix + "submit_date"].isoformat()

    if s.publish_date is not None:
        data["published_date"] = s[prefix + "publish_date"].isoformat()
    else:
        data["published_date"] = None

    return data


def topic(t, extended=True):
    data = dict()

    data["id"] = t.id

    data["slug"] = t.slug
    data["title"] = t.title
    data["icon"] = t.icon

    if extended:
        data["description"] = t.desc

        data["stories_count"] = t.stories_count

    return data


def comment(c, extended=True):
    data = dict()

    data["id"] = identifier.to36(c.id)
    data["parent_id"] = c.parent_id
    data["author_id"] = c.author_id

    if extended:
        data["story_id"] = c.story_id

    data["content"] = c.content

    data["likes_count"] = c.likes_count
    data["comments_count"] = c.comments_count

    data["submitted_date"] = c.submitted_date.isoformat()

    if c.edited_date is not None:
        data["edited_date"] = c.edited_date.isoformat()

    return data
