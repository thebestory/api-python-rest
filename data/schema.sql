--
-- TABLES
--

CREATE TABLE comment_likes (
  user_id     INTEGER                                NOT NULL,
  comment_id  INTEGER                                NOT NULL,
  state       BOOLEAN                                NOT NULL,
  "timestamp" TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE comments (
  id             INTEGER                                NOT NULL,
  parent_id      INTEGER,
  author_id      INTEGER                                NOT NULL,
  story_id       INTEGER                                NOT NULL,
  content        TEXT                                   NOT NULL,
  likes_count    INTEGER DEFAULT 0                      NOT NULL,
  comments_count INTEGER DEFAULT 0                      NOT NULL,
  is_removed     BOOLEAN DEFAULT FALSE                  NOT NULL,
  submitted_date TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  edited_date    TIMESTAMP WITH TIME ZONE
);

CREATE TABLE stories (
  id             INTEGER                                NOT NULL,
  author_id      INTEGER                                NOT NULL,
  topic_id       INTEGER                                NOT NULL,
  content        TEXT                                   NOT NULL,
  likes_count    INTEGER DEFAULT 0                      NOT NULL,
  comments_count INTEGER DEFAULT 0                      NOT NULL,
  is_approved    BOOLEAN DEFAULT FALSE                  NOT NULL,
  is_removed     BOOLEAN DEFAULT FALSE                  NOT NULL,
  submitted_date TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  edited_date    TIMESTAMP WITH TIME ZONE,
  published_date TIMESTAMP WITH TIME ZONE
);

CREATE TABLE story_likes (
  user_id     INTEGER                                NOT NULL,
  story_id    INTEGER                                NOT NULL,
  state       BOOLEAN                                NOT NULL,
  "timestamp" TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE topics (
  id            INTEGER               NOT NULL,
  slug          CHARACTER VARYING(32) NOT NULL,
  title         CHARACTER VARYING(64) NOT NULL,
  description   TEXT                  NOT NULL,
  icon          CHARACTER VARYING(16),
  stories_count INTEGER DEFAULT 0     NOT NULL
);

CREATE TABLE users (
  id             INTEGER               NOT NULL,
  username       CHARACTER VARYING(32) NOT NULL,
  stories_count  INTEGER DEFAULT 0     NOT NULL,
  comments_count INTEGER DEFAULT 0     NOT NULL,
  likes_count    INTEGER DEFAULT 0     NOT NULL
);

--
-- SEQUENCES
--

CREATE SEQUENCE comments_id_seq START WITH 466561 /* a001 */ INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE stories_id_seq START WITH 466561 /* a001 */ INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE topics_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE users_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;

--
-- SEQUENCES OWNERS
--

ALTER SEQUENCE comments_id_seq OWNED BY comments.id;
ALTER SEQUENCE stories_id_seq OWNED BY stories.id;
ALTER SEQUENCE topics_id_seq OWNED BY topics.id;
ALTER SEQUENCE users_id_seq OWNED BY users.id;

--
-- SEQUENCES OWNERS DEFAULTS
--

ALTER TABLE ONLY comments
  ALTER COLUMN id SET DEFAULT nextval('comments_id_seq' :: REGCLASS);

ALTER TABLE ONLY stories
  ALTER COLUMN id SET DEFAULT nextval('stories_id_seq' :: REGCLASS);

ALTER TABLE ONLY topics
  ALTER COLUMN id SET DEFAULT nextval('topics_id_seq' :: REGCLASS);

ALTER TABLE ONLY users
  ALTER COLUMN id SET DEFAULT nextval('users_id_seq' :: REGCLASS);

---
--- PKs
---

ALTER TABLE ONLY comments
  ADD CONSTRAINT comments_pkey PRIMARY KEY (id);

ALTER TABLE ONLY stories
  ADD CONSTRAINT stories_pkey PRIMARY KEY (id);

ALTER TABLE ONLY topics
  ADD CONSTRAINT topics_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users
  ADD CONSTRAINT users_pkey PRIMARY KEY (id);

---
--- INDEXES
---

CREATE INDEX comment_likes_comment_id_index
  ON comment_likes USING BTREE (comment_id);

CREATE INDEX comment_likes_user_id_comment_id_index
  ON comment_likes USING BTREE (user_id, comment_id);

CREATE INDEX comments_author_id_index
  ON comments USING BTREE (author_id);

CREATE INDEX comments_parent_id_index
  ON comments USING BTREE (parent_id);

CREATE INDEX comments_story_id_index
  ON comments USING BTREE (story_id);

CREATE INDEX stories_author_id_index
  ON stories USING BTREE (author_id);

CREATE INDEX stories_topic_id_index
  ON stories USING BTREE (topic_id);

CREATE INDEX story_likes_story_id_index
  ON story_likes USING BTREE (story_id);

CREATE INDEX story_likes_user_id_story_id_index
  ON story_likes USING BTREE (user_id, story_id);

CREATE UNIQUE INDEX topics_slug_uindex
  ON topics USING BTREE (slug);

CREATE UNIQUE INDEX users_username_uindex
  ON users USING BTREE (username);

---
--- FKs
---

ALTER TABLE ONLY comment_likes
  ADD CONSTRAINT comment_likes_comments_id_fk FOREIGN KEY (comment_id) REFERENCES comments (id);

ALTER TABLE ONLY comment_likes
  ADD CONSTRAINT comment_likes_users_id_fk FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE ONLY comments
  ADD CONSTRAINT comments_author_id_fk FOREIGN KEY (author_id) REFERENCES users (id);

ALTER TABLE ONLY comments
  ADD CONSTRAINT comments_parent_id_fk FOREIGN KEY (parent_id) REFERENCES comments (id);

ALTER TABLE ONLY comments
  ADD CONSTRAINT comments_story_id_fk FOREIGN KEY (story_id) REFERENCES stories (id);

ALTER TABLE ONLY stories
  ADD CONSTRAINT stories_topics_id_fk FOREIGN KEY (topic_id) REFERENCES topics (id);

ALTER TABLE ONLY stories
  ADD CONSTRAINT stories_users_id_fk FOREIGN KEY (author_id) REFERENCES users (id);

ALTER TABLE ONLY story_likes
  ADD CONSTRAINT story_likes_stories_id_fk FOREIGN KEY (story_id) REFERENCES stories (id);

ALTER TABLE ONLY story_likes
  ADD CONSTRAINT story_likes_users_id_fk FOREIGN KEY (user_id) REFERENCES users (id);
