"""
The Bestory Project
"""

from asyncpg.connection import Connection

from tbs.lib.stores import user as user_store


users = [
    {'username': 'thebestory', 'email': 'thebestory@thebestory.com', 'password': 'thebestory'},
    {'username': 'woofilee', 'email': 'woofilee@thebestory.com', 'password': 'thebestory'},
    {'username': 'alex', 'email': 'alex@thebestory.com', 'password': 'thebestory'},
    {'username': 'oktai', 'email': 'oktai@thebestory.com', 'password': 'thebestory'},
    {'username': 'bytonishe', 'email': 'bytonishe@thebestory.com', 'password': 'thebestory'}
]

topics = [
    {'title': 'Weird', 'slug': 'weird', 'icon': '9406QtVe637', 'is_active': True, 'description': 'All of us are weird, but there might be someone, whose story will make your eyes pop out. Check it out right now!'},
    {'title': 'Love', 'slug': 'love', 'icon': '8utqsEYq596', 'is_active': True, 'description': 'Do you have doubts about love existence? We can assure you it does exist. Check out the evidence of it in the touching stories of our members!'},
    {'title': 'Funny', 'slug': 'funny', 'icon': 'c407w1H03A0', 'is_active': True, 'description': 'We all know that everyone loves to laugh. So, why would you restrain yourselves from it? Enjoy hilarious moments from our subscribers lives.'},
    {'title': 'Intimate', 'slug': 'intimate', 'icon': 'cWiepIBqmtJ', 'is_active': True, 'description': 'Some say sex brings people together. Now it\'s time to test this statement and read a couple of hot stories from our members.'},
    {'title': 'Happiness', 'slug': 'happiness', 'icon': '9ilbmJGoCFr', 'is_active': True, 'description': 'Here you will see what (pushes us forward) and makes us try again. What makes our life meaningful. The moments when we are endlessly happy.'},
    {'title': 'Lifehack', 'slug': 'lifehack', 'icon': 'c00fM2X0Iw1', 'is_active': True, 'description': 'We guess you could not even imagine that there is (an easier approach to some problems)such an easy and satisfying way to do it. Here our members will share it with you!'},
    {'title': 'Good', 'slug': 'gooddeeds', 'icon': 'd7wmKsG0iQe', 'is_active': True, 'description': 'There are tons of great people in the world around us, even if it is hard to see. Read some of these stories and restore your perhaps lost faith in humanity.'},
    {'title': 'Dreams', 'slug': 'dreams', 'icon': '9kBiF8KM3L2', 'is_active': True, 'description': 'What can you see, feel or do while you are asleep? Anything you have ever thought about and beyond that. Find out what others dreams are like!'},
    {'title': 'Scary', 'slug': 'scary', 'icon': 'c407w1K03A0', 'is_active': True, 'description': 'Sometimes our life isn’t as good as we\'d like it to be. Moreover, there are certain moments when we are petrified. Read these stories about such situations, if you dare.'},
    {'title': 'Sad', 'slug': 'sad', 'icon': 'c407w1H03M0', 'is_active': True, 'description': 'If you feel down or it is too early for you to move on, check our users stories who are in the same boat with you.'},
    {'title': 'Daydreams', 'slug': 'daydreams', 'icon': 'c6ZblE$m3o5', 'is_active': True, 'description': 'You probably need just a little push to become greater than you are now. Maybe some of these stories will help you to pursue your own dreams.'}
]

stories = [
    {'author': 'woofilee', 'topic': 'weird', 'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'That is the end. Saw an ad where a heart gets out off a chest and goes to a balcony, plays a guitar and asks to feed itself with brand sausage. Then kisses a girl in the nose. Jeez.'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'I work in a hospital, in the reception ward. So, there comes a patient with a severed finger saying: \"Could you not sew that please, I\'ll fill it with amber and make a necklace.\" All the ward got stunned!'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'Long story short, a few minutes ago I\'m coming home from a bus stop, a woman approaches and yells \"You have the pox, young lady\" and then runs away. I even like these weirdos, they give a reason to reflect a bit.'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'We have quite a bizarre professor in our uni. After every single class, when nobody\'s around, he starts licking the blackboard in chalk. GOD DAMN BLACKBOARD!'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'My gf calls my bristle \"Edward\". And every time when I\'m not shaved she touches my chin and with all the seriousness and equanimity which is inherent in her says to me \"You need to get rid of Edward. Try not to leave any witnesses.\"'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'Saw a girl in a bus yesterday with a SAT tests book, came closer to pay and found out that behind the book she had a phone with a gay-porn video going on.'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'My mom recently told a story: she has a friend who lives with her kid in Europe. The friend took the kid on holidays to a grandmother somewhere in Russia. So, the boy decided to play on the tablet as usual for what he got a cuff from the granny. Fully surprised he looked at her and then said that he would go to the court and sue her for the child abuse. The grandmother gave another one as a response saying \"Not in this country!\". So true)'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'Everyone, I guess, has such things that bring good luck, talismans so to say. One has a hare\'s-foot, second – four-leaf clover, third has something else. It may be very ordinary, but sometimes it is just tooo weird. But the fact that a friend of mine has a woman\'s tampon which he always takes with him wherever he goes – that\'s what I never would\'ve expected.'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'Bought a few chicken\'s heads today. I put on one chicken head on each finger of one hand and made rock to the music. Here goes the chicken disco!'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'Today caught a kid, a boy, two years old at best. On the roadway. His mother didn\'t even realize. He showed me where she was. I brought her the kid, told him to turn away and gave her a real slap in the face. I Just couldn\'t resist.'},
    {'author': 'thebestory', 'topic': 'love', 'content': 'It\'s hard to be a bold and bearded princess. Especially when you a 57 yo man. But grandpa\'s ready to do anything for his grandbaby.'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'I do appreciate the time I sleep, so I never set the alarm for 6-30, I go 6-31 instead.'},
    {'author': 'thebestory', 'topic': 'intimate', 'content': 'Turned on the TV to watch some porn and have a good time all alone. But overdid a bit with the volume and didn\'t even notice when the mum came. She knocks on my door, I roll in a blanket ASAP, then she comes in and says: \"Sweetheart, are you all right? What\'s that noise?\". \"Oh, that\'s nothing mum, I\'m just lying and breathing\". And i breathe in and breath out loudly and deeply a few times. Damn genius!'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'I came home and heard a shrill \"Meeeeeeoooow\". Called my cat \"Kitty! kitty, where are you?\". I sat on a couch and heard again \"Meeeeeeeeeooooooow\". I peeped in it and found my 19 yo bro! How did he get there? Hell knows. But one thing i know now for sure – my brother is a jerk.'},
    {'author': 'thebestory', 'topic': 'happiness', 'content': 'This is the third day of my vacation. I set the alarm for 6-00 in the morning and when it goes off I just turn it off, roll over with a real delight and fall asleep again with a smile on my face. Hell yeah.'},
    {'author': 'thebestory', 'topic': 'happiness', 'content': 'Lost my fingers on one hand 5 years ago, all of them except for the middle one. Everyone sympathizes and feel so sorry for me, saying like it must be hard to go on. Come on you guys! I give the finger to people every day but yet they don\'t even know about it:) I am absolutely happy, no need for you to be sorry:)'},
    {'author': 'thebestory', 'topic': 'lifehack', 'content': 'In the morning my bf asked me to make him cream soup, but later that day we had a quarrel and he left. In short I gobbled the whole pot during the night and even forgot about my man:) Eating is bliss:))'},
    {'author': 'thebestory', 'topic': 'lifehack', 'content': 'My mum is a genius. I just broke up with a guy, you know, weep, tears, hysterics. So she comes to me with a laptop and shows Ducane diet. I ask her why? \"Honey, as soon as you are on a diet, all your thoughts will be devoted to the food and none to your bastards\". G E N I U S!'},
    {'author': 'thebestory', 'topic': 'gooddeeds', 'content': 'I\'m a bartender. If I see that some queer fish put the moves to a pretty girl and tries to liquor her then I don\'t add alcohol to her cocktails at all, so that she wouldn\'t go anywhere with the guy and nothing bad happens.'},
    {'author': 'thebestory', 'topic': 'dreams', 'content': 'I had a dream tonight where my husband confessed to me that he was a girl. Got awoke from my own inextinguishable laughter, but then I felt kinda sad. I put my hand in his pants and checked. Everything was fine. Only then I calmed down and felt asleep.'},
    {'author': 'thebestory', 'topic': 'happiness', 'content': 'I live with my boyfriend. We are both from the children\'s home. Sometimes we barely can make ends meet and we also often pay the rent way later than we have to (it\'s okay cause our landlady is really nice and kind to us). We have our favorite sausages for tonight\'s supper but we know how not to complain about anything and we love each other so much.'},
    {'author': 'thebestory', 'topic': 'dreams', 'content': 'I often see dreams about zombie apocalypse. And tonight I saved my relatives again. Using tape. Sticky tape. Well, fine. I just blocked up the door with it. \"Sticky tape is always there to help\".'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'The most extreme sport is a fast cleaning in 5 minutes before mom comes.'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'Yesterday my friend felt asleep during the lesson, well, seems like nothing special at all... but yet she is a TEACHER!'},
    {'author': 'thebestory', 'topic': 'scary', 'content': 'I will take everything from you. Your sleeping. Food. Games. Friends. Series. Brains. (C) The studying'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'When my ex was moving out he poured out the whole kettle of water on my bed, stripped a bunch of wallpapers, burnt down the Xmas tree in the bathroom and took away my vibrator! What the hell does he need it for? :)'},
    {'author': 'thebestory', 'topic': 'weird', 'content': 'In lots of movies the guy after betrayal usually has a lipstick print on his shirt. I never understood that. Why would you even kiss a man in a shirt?!'},
    {'author': 'thebestory', 'topic': 'daydreams', 'content': 'You know, sometimes you don\'t have the guts for a long time to do something cause you\'re afraid that you\'ll ruin everything. But then you overcome yourself and you finally do what you always wanted and everything\'s just great! So, all this is not about me.'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'My husband is a virologist. Last Saturday after his night shift he went to the lake. Of course, he took me and the kids, we had a barbeque till the night, and then there came a whole bunch of mosquitoes, but he didn\'t get lost and brought us four biohazard suits. People all around us then started leaving as soon as they\'d seen us :)'},
    {'author': 'thebestory', 'topic': 'funny', 'content': 'The only person that can be faster than a man with 1% on his phone is one that\'s running to a yawning cat to put his finger in the cat\'s mouth.'}
]


async def insert_users(conn: Connection):
    for user in users:
        user_store.create(**user, conn=conn)


async def insert_topics(conn: Connection):
    pass


async def insert_stories(conn: Connection):
    pass


async def insert(conn: Connection):
    insert_users(conn)
    insert_topics(conn)
    insert_stories(conn)


async def clear(conn: Connection):
    pass
