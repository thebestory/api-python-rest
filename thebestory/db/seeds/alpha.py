"""
The Bestory Project
"""

import datetime
import pytz
from asyncpgsa.pool import SAPool

from thebestory.app.models import stories, topics, users


async def seed(db: SAPool):
    users_list = [
        "thebestory",
        "woofilee",
        "oktai",
        "bytonishe",
    ]

    topics_list = [
        ("funny", "Funny"),
        ("sad", "Sad"),
        ("vulgar", "Vulgar"),
        ("terrible", "Terrible"),
        ("strange", "Strange"),
        ("lifehack", "Lifehack"),
        ("dreams", "Dreams"),
        ("kindly", "Kindly"),
        ("happiness", "Happiness"),
        ("love", "Love"),
        ("other", "Other"),
    ]

    stories_list = [
        (
            1,  # author_ d
            11,  # topic id
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam "
            "vestibulum velit a placerat ultrices. Proin suscipit dolor risus, "
            "sed sodales felis faucibus sed. Suspendisse facilisis, eros vitae "
            "pretium egestas, mi eros vehicula elit, ac porttitor sapien nisl "
            "vitae orci. Interdum et malesuada fames ac ante ipsum primis in "
            "faucibus. Cras venenatis rhoncus porttitor. Nulla ac blandit "
            "purus, nec pharetra ex. Donec libero ex, egestas a euismod eu, "
            "malesuada sed erat. Suspendisse auctor, tortor vitae tincidunt "
            "volutpat, dolor orci consequat ligula, a efficitur est urna "
            "hendrerit ante. Donec quis euismod turpis. Vivamus sed felis in "
            "est pretium bibendum nec eu lorem. Sed porta massa vel ligula "
            "interdum, auctor imperdiet odio fringilla. Phasellus bibendum "
            "lobortis malesuada. Praesent ultricies justo sed tortor laoreet, "
            "at sollicitudin sapien laoreet. Nunc lacinia, erat in ornare "
            "cursus, nunc augue suscipit dui, nec venenatis dui felis nec est. "
            "Proin non vehicula neque. Duis congue tincidunt diam eu ornare."
        ),
        (
            1,  # author id
            5,  # topic id
            "We have quite a bizarre professor in our uni. After every single "
            "class, when nobody’s around, he starts licking the blackboard in "
            "chalk. GOD DAMN BLACKBOARD!"
        ),
        (
            1,  # author id
            1,  # topic id
            "My gf calls my bristle \"Edward\". And every time when I’m not "
            "shaved she touches my chin and with all the seriousness and "
            "equanimity which is inherent in her says to me \"You need to get "
            "rid of Edward. Try not to leave any witnesses.\"."
        ),
        (
            1,  # author id
            6,  # topic id
            "Saw a girl in a bus yesterday with a SAT tests book, came closer "
            "to pay and found out that behind the book she had a phone with a "
            "gay-porn video going on."
        ),
        (
            1,  # author id
            5,  # topic id
            "That is the end. Saw an ad where a heart gets out off a chest and "
            "goes to a balcony, plays a guitar and asks to feed itself with "
            "brand sausage. Then kisses a girl in the nose. Jeez."
        ),
        (
            1,  # author id
            5,  # topic id
            "I work in a hospital, in the reception ward. So, there comes a "
            "patient with a severed finger saying: \"Could you not sew that "
            "please, I’ll fill it with amber and make a necklace.\". All the "
            "ward got stunned!"
        ),
        (
            1,  # author id
            5,  # topic id
            "Long story short, a few minutes ago I’m coming home from a bus "
            "stop, a woman approaches and yells \"You have the pox, young "
            "lady\" and then runs away. I even like these weirdos, they give a "
            "reason to reflect a bit."
        ),
        (
            1,  # author id
            1,  # topic id
            "My mom recently told a story: she has a friend who lives with her "
            "kid in Europe. The friend took the kid on holidays to a "
            "grandmother somewhere in Russia. So, the boy decided to play on "
            "the tablet as usual for what he got a cuff from the granny. Fully "
            "surprised he looked at her and then said that he would go to the "
            "court and sue her for the child abuse. The grandmother gave "
            "another one as a response saying \"Not in this country!\". So "
            "true)"
        ),
        (
            1,  # author id
            5,  # topic id
            "Everyone, I guess, has such things that bring good luck, "
            "talismans so to say. One has a hare’s-foot, second – four-leaf "
            "clover, third has something else. It may be very ordinary, but "
            "sometimes it is just tooo weird. But the fact that a friend of "
            "mine has a woman’s tampon which he always takes with him wherever "
            "he goes – that’s what I never would’ve expected."
        ),
        (
            1,  # author id
            5,  # topic id
            "Bought a few chicken’s heads today. I put on one chicken head on "
            "each finger of one hand and made rock to the music. Here goes the "
            "chicken disco!"
        ),
        (
            1,  # author id
            4,  # topic id
            "Today caught a kid, a boy, two years old top. On the roadway. His "
            "mother didn’t even realise. He showed me where she was. I brought "
            "her the kid, told him to turn away and gave her a real slap in "
            "the face. I Just couldn’t resist."
        ),
    ]

    async def seed_users():
        print("Seeding users...")

        async with db.transaction() as conn:
            for username in users_list:
                print("-", username)

                await conn.fetchval(users.insert().values(
                    username=username
                ))

    async def seed_topics():
        print("Seeding topics...")

        def count_stories(topic_id):
            cnt = 0

            for story in stories_list:
                if story[1] == topic_id:
                    cnt += 1

            return cnt

        async with db.transaction() as conn:
            for slug, title in topics_list:
                print("-", title)

                await conn.fetchval(topics.insert().values(
                    title=title,
                    slug=slug,
                    desc="",
                    icon="",
                    stories_count=count_stories(
                        topics_list.index((slug, title)))
                ))

    async def seed_stories():
        print("Seeding stories...")

        async with db.transaction() as conn:
            for author_id, topic_id, content in stories_list:
                print("-", author_id, ":", topic_id)

                await conn.fetchval(
                    stories.insert().values(
                        author_id=author_id,
                        topic_id=topic_id,
                        content=content,
                        submit_date=datetime.datetime.utcnow().replace(
                            tzinfo=pytz.utc),
                        publish_date=datetime.datetime.utcnow().replace(
                            tzinfo=pytz.utc)
                    ))

    await seed_users()
    await seed_topics()
    await seed_stories()
