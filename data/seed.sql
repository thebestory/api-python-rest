---
--- USERS
---

INSERT INTO users (username) VALUES ('woofilee');
INSERT INTO users (username) VALUES ('thebestory');
INSERT INTO users (username) VALUES ('oktai');
INSERT INTO users (username) VALUES ('bytonishe');
INSERT INTO users (username) VALUES ('anonymous');
INSERT INTO users (username) VALUES ('alex');

---
--- TOPICS
---

INSERT INTO topics (slug, title, description, icon, is_public) VALUES ('all', 'All',
                                                                       'All topics in one place. Yes, you can combine it. But... why you''re reading this? It''s pseudo topic...',
                                                                       '',
                                                                       FALSE);

INSERT INTO topics (slug, title, description, icon) VALUES ('weird', 'Weird',
                                                            'We all are weird, but there might be someone whose story will make your eyes pop out. Check it out right now!',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('love', 'Love',
                                                            'Are you in doubt whether love exists or not? We assure you it does, all the evidence in the touching stories by our members!',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('funny', 'Funny',
                                                            'We all know we are fond of laughing. So, why would we restrain ourselves from it? Enjoy the hilarious moments of lives of our subscribers.',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('intimate', 'Intimate',
                                                            'They say sex brings people together. Now it’s time to check this and read a couple of hot stories from our members.',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('happiness', 'Happiness',
                                                            'Here you will see what makes us try again and again, what makes our lives meaningful. The moments when we are infinitely happy.',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('lifehack', 'Lifehack',
                                                            'We guess you couldn’t even imagine that there is such an easy and satisfying way to do it. Here, our members will show you!',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('gooddeeds', 'Good deeds',
                                                            'Read the stories of our members and make yourself sure that our world is full of people with hearts of gold!',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('dreams', 'Dreams',
                                                            'What can you see, feel or make while you are asleep? Anything you have ever thought of and even more. Find out what others have dreamt of!',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('scary', 'Scary',
                                                            'Sometimes our lives aren’t as good as we’d like to. But there are certain moments when we just get petrified. Read the stories about it, if you dare.',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('sad', 'Sad',
                                                            'Not available',
                                                            '');
INSERT INTO topics (slug, title, description, icon) VALUES ('daydreams', 'Daydreams',
                                                            'Not available',
                                                            '');

---
--- STORIES
---

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'woofilee'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        TRUE, '2016-12-01 01:13:46.638485 +03:00', '2016-12-01 01:13:46.638485 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'That is the end. Saw an ad where a heart gets out off a chest and goes to a balcony, plays a guitar and asks to feed itself with brand sausage. Then kisses a girl in the nose. Jeez.',
        TRUE, '2016-12-01 19:48:15.667776 +03:00', '2016-12-01 19:48:15.667776 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'I work in a hospital, in the reception ward. So, there comes a patient with a severed finger saying: "Could you not sew that please, I''ll fill it with amber and make a necklace." All the ward got stunned!',
        TRUE, '2016-12-01 19:51:59.244625 +03:00', '2016-12-01 19:51:59.244625 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'Long story short, a few minutes ago I''m coming home from a bus stop, a woman approaches and yells "You have the pox, young lady" and then runs away. I even like these weirdos, they give a reason to reflect a bit.',
        TRUE, '2016-12-01 19:58:02.533970 +03:00', '2016-12-01 19:58:02.533970 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'We have quite a bizarre professor in our uni. After every single class, when nobody''s around, he starts licking the blackboard in chalk. GOD DAMN BLACKBOARD!',
        TRUE, '2016-12-02 00:43:42.111000 +03:00', '2016-12-02 00:43:47.164000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'My gf calls my bristle "Edward". And every time when I''m not shaved she touches my chin and with all the seriousness and equanimity which is inherent in her says to me "You need to get rid of Edward. Try not to leave any witnesses."',
        TRUE, '2016-12-02 00:44:18.759000 +03:00', '2016-12-02 00:44:21.085000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'Saw a girl in a bus yesterday with a SAT tests book, came closer to pay and found out that behind the book she had a phone with a gay-porn video going on.',
        TRUE, '2016-12-02 00:45:39.062000 +03:00', '2016-12-02 00:45:42.815000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'My mom recently told a story: she has a friend who lives with her kid in Europe. The friend took the kid on holidays to a grandmother somewhere in Russia. So, the boy decided to play on the tablet as usual for what he got a cuff from the granny. Fully surprised he looked at her and then said that he would go to the court and sue her for the child abuse. The grandmother gave another one as a response saying "Not in this country!". So true)',
        TRUE, '2016-12-02 00:47:35.447000 +03:00', '2016-12-02 00:47:37.811000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'Everyone, I guess, has such things that bring good luck, talismans so to say. One has a hare''s-foot, second – four-leaf clover, third has something else. It may be very ordinary, but sometimes it is just tooo weird. But the fact that a friend of mine has a woman''s tampon which he always takes with him wherever he goes – that''s what I never would''ve expected.',
        TRUE, '2016-12-02 00:50:35.647000 +03:00', '2016-12-02 00:50:38.253000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'Bought a few chicken''s heads today. I put on one chicken head on each finger of one hand and made rock to the music. Here goes the chicken disco!',
        TRUE, '2016-12-02 00:54:11.183000 +03:00', '2016-12-02 00:54:14.277000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'Today caught a kid, a boy, two years old at best. On the roadway. His mother didn''t even realize. He showed me where she was. I brought her the kid, told him to turn away and gave her a real slap in the face. I Just couldn''t resist.',
        TRUE, '2016-12-02 00:54:57.194000 +03:00', '2016-12-02 00:54:59.778000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'love'),
        'It''s hard to be a bold and bearded princess. Especially when you a 57 yo man. But grandpa''s ready to do anything for his grandbaby.',
        TRUE, '2016-12-02 00:56:07.818000 +03:00', '2016-12-02 00:56:09.928000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'I do appreciate the time I sleep, so I never set the alarm for 6-30, I go 6-31 instead.',
        TRUE, '2016-12-02 00:56:42.201000 +03:00', '2016-12-02 00:56:44.602000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'intimate'),
        'Turned on the TV to watch some porn and have a good time all alone. But overdid a bit with the volume and didn''t even notice when the mum came. She knocks on my door, I roll in a blanket ASAP, then she comes in and says: "Sweetheart, are you all right? What''s that noise?". "Oh, that''s nothing mum, I''m just lying and breathing". And i breathe in and breath out loudly and deeply a few times. Damn genius!',
        TRUE, '2016-12-02 00:58:39.197000 +03:00', '2016-12-02 00:58:41.354000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'I came home and heard a shrill "Meeeeeeoooow". Called my cat "Kitty! kitty, where are you?". I sat on a couch and heard again "Meeeeeeeeeooooooow". I peeped in it and found my 19 yo bro! How did he get there? Hell knows. But one thing i know now for sure – my brother is a jerk.',
        TRUE, '2016-12-02 00:59:49.990000 +03:00', '2016-12-02 00:59:51.994000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'happiness'),
        'This is the third day of my vacation. I set the alarm for 6-00 in the morning and when it goes off I just turn it off, roll over with a real delight and fall asleep again with a smile on my face. Hell yeah.',
        TRUE, '2016-12-02 01:00:24.074000 +03:00', '2016-12-02 01:00:26.248000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'happiness'),
        'Lost my fingers on one hand 5 years ago, all of them except for the middle one. Everyone sympathizes and feel so sorry for me, saying like it must be hard to go on. Come on you guys! I give the finger to people every day but yet they don''t even know about it:) I am absolutely happy, no need for you to be sorry:)',
        TRUE, '2016-12-02 01:01:19.803000 +03:00', '2016-12-02 01:01:22.178000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'lifehack'),
        'In the morning my bf asked me to make him cream soup, but later that day we had a quarrel and he left. In short I gobbled the whole pot during the night and even forgot about my man:) Eating is bliss:))',
        TRUE, '2016-12-02 01:01:48.081000 +03:00', '2016-12-02 01:01:50.489000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'lifehack'),
        'My mum is a genius. I just broke up with a guy, you know, weep, tears, hysterics. So she comes to me with a laptop and shows Ducane diet. I ask her why? "Honey, as soon as you are on a diet, all your thoughts will be devoted to the food and none to your bastards". G E N I U S!',
        TRUE, '2016-12-02 01:02:19.050000 +03:00', '2016-12-02 01:02:21.218000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'good-deeds'),
        'I''m a bartender. If I see that some queer fish put the moves to a pretty girl and tries to liquor her then I don''t add alcohol to her cocktails at all, so that she wouldn''t go anywhere with the guy and nothing bad happens.',
        TRUE, '2016-12-02 01:04:20.752000 +03:00', '2016-12-02 01:04:23.407000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'dreams'),
        'I had a dream tonight where my husband confessed to me that he was a girl. Got awoke from my own inextinguishable laughter, but then I felt kinda sad. I put my hand in his pants and checked. Everything was fine. Only then I calmed down and felt asleep.',
        TRUE, '2016-12-02 01:05:09.212000 +03:00', '2016-12-02 01:05:12.346000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'happiness'),
        'I live with my boyfriend. We are both from the children''s home. Sometimes we barely can make ends meet and we also often pay the rent way later than we have to (it''s okay cause our landlady is really nice and kind to us). We have our favorite sausages for tonight''s supper but we know how not to complain about anything and we love each other so much.',
        TRUE, '2016-12-02 01:06:03.837000 +03:00', '2016-12-02 01:06:06.053000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'dreams'),
        'I often see dreams about zombie apocalypse. And tonight I saved my relatives again. Using tape. Sticky tape. Well, fine. I just blocked up the door with it. "Sticky tape is always there to help".',
        TRUE, '2016-12-02 01:06:44.803000 +03:00', '2016-12-02 01:06:46.954000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'The most extreme sport is a fast cleaning in 5 minutes before mom comes.',
        TRUE, '2016-12-02 01:07:06.431000 +03:00', '2016-12-02 01:07:09.206000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'Yesterday my friend felt asleep during the lesson, well, seems like nothing special at all... but yet she is a TEACHER!',
        TRUE, '2016-12-02 01:08:37.592000 +03:00', '2016-12-02 01:08:39.739000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'scary'),
        'I will take everything from you. Your sleeping. Food. Games. Friends. Series. Brains. © The studying',
        TRUE, '2016-12-02 01:09:05.261000 +03:00', '2016-12-02 01:09:08.539000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'When my ex was moving out he poured out the whole kettle of water on my bed, stripped a bunch of wallpapers, burnt down the Xmas tree in the bathroom and took away my vibrator! What the hell does he need it for? :)',
        TRUE, '2016-12-02 01:09:39.794000 +03:00', '2016-12-02 01:09:41.959000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'weird'),
        'In lots of movies the guy after betrayal usually has a lipstick print on his shirt. I never understood that. Why would you even kiss a man in a shirt?!',
        TRUE, '2016-12-02 01:12:26.692000 +03:00', '2016-12-02 01:12:29.465000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'daydreams'),
        'You know, sometimes you don''t have the guts for a long time to do something cause you''re afraid that you''ll ruin everything. But then you overcome yourself and you finally do what you always wanted and everything''s just great! So, all this is not about me.',
        TRUE, '2016-12-02 01:13:05.243000 +03:00', '2016-12-02 01:13:08.202000 +03:00');

INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'My husband is a virologist. Last Saturday after his night shift he went to the lake. Of course, he took me and the kids, we had a barbeque till the night, and then there came a whole bunch of mosquitoes, but he didn''t get lost and brought us four biohazard suits. People all around us then started leaving as soon as they''d seen us :)',
        TRUE, '2016-12-02 01:13:28.068000 +03:00', '2016-12-02 01:13:30.119000 +03:00');


INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
VALUES ((SELECT users.id
         FROM users
         WHERE users.username = 'thebestory'),
        (SELECT topics.id
         FROM topics
         WHERE topics.slug = 'funny'),
        'The only person that can be faster than a man with 1% on his phone is one that''s running to a yawning cat to put his finger in the cat''s mouth.',
        TRUE, '2016-12-02 01:13:49.583000 +03:00', '2016-12-02 01:13:52.407000 +03:00');

-- weird
-- love
-- funny
-- intimate
-- happiness
-- lifehack
-- good-deeds
-- dreams
-- scary
-- sad
-- daydreams
--
-- INSERT INTO stories (author_id, topic_id, content, is_approved, submitted_date, published_date)
-- VALUES ((SELECT users.id
--          FROM users
--          WHERE users.username = 'thebestory'),
--         (SELECT topics.id
--          FROM topics
--          WHERE topics.slug = ''),
--         '',
--         TRUE, '', '');

---
--- COUNTERS
---

UPDATE users
SET stories_count = (
  SELECT count(*)
  FROM stories
  WHERE stories.author_id = users.id
);

UPDATE topics
SET stories_count = (
  SELECT count(*)
  FROM stories
  WHERE stories.topic_id = topics.id
);
