--
-- TABLES
--

CREATE TABLE ids (
  id                  BIGINT                                 NOT NULL,
  type                CHARACTER VARYING(32)                  NOT NULL
);

CREATE TABLE users (
  id                  BIGINT                                 NOT NULL,
  username            CHARACTER VARYING(32)                  NOT NULL,
  email               CHARACTER VARYING(32)                  NOT NULL,
  password            CHARACTER VARYING(255)                 NOT NULL,
  comments_count      INTEGER DEFAULT 0                      NOT NULL,
  reactions_count     INTEGER DEFAULT 0                      NOT NULL,
  stories_count       INTEGER DEFAULT 0                      NOT NULL,
  registered_date     TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE topics (
  id            BIGINT                NOT NULL,
  title         CHARACTER VARYING(64) NOT NULL,
  slug          CHARACTER VARYING(32) NOT NULL,
  description   TEXT                  NOT NULL,
  icon          CHARACTER VARYING(16) NOT NULL,
  stories_count INTEGER DEFAULT 0     NOT NULL,
  is_active     BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE comments (
  id              BIGINT                                 NOT NULL,
  author_id       BIGINT                                 NOT NULL,
  root_id         BIGINT                                 NOT NULL,
  parent_id       BIGINT                                 NOT NULL,
  content         TEXT                                   NOT NULL,
  comments_count  INTEGER DEFAULT 0                      NOT NULL,
  reactions_count INTEGER DEFAULT 0                      NOT NULL,
  is_published    BOOLEAN DEFAULT FALSE                  NOT NULL,
  is_removed      BOOLEAN DEFAULT FALSE                  NOT NULL,
  submitted_date  TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  published_date  TIMESTAMP WITH TIME ZONE,
  edited_date     TIMESTAMP WITH TIME ZONE
);

CREATE TABLE likes (
  user_id      BIGINT                                 NOT NULL,
  object_id    BIGINT                                 NOT NULL,
  valid        BOOLEAN DEFAULT TRUE                   NOT NULL,
  added_date   TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  removed_date TIMESTAMP WITH TIME ZONE
);

CREATE TABLE stories (
  id              BIGINT                                 NOT NULL,
  author_id       BIGINT                                 NOT NULL,
  topic_id        BIGINT,
  content         TEXT                                   NOT NULL,
  comments_count  INTEGER DEFAULT 0                      NOT NULL,
  reactions_count INTEGER DEFAULT 0                      NOT NULL,
  is_published    BOOLEAN DEFAULT FALSE                  NOT NULL,
  is_removed      BOOLEAN DEFAULT FALSE                  NOT NULL,
  submitted_date  TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
  published_date  TIMESTAMP WITH TIME ZONE,
  edited_date     TIMESTAMP WITH TIME ZONE
);


---
--- PKs
---

ALTER TABLE ONLY ids
  ADD CONSTRAINT ids_pkey        PRIMARY KEY (id);

ALTER TABLE ONLY users
  ADD CONSTRAINT users_pkey      PRIMARY KEY (id);

ALTER TABLE ONLY topics
  ADD CONSTRAINT topics_pkey     PRIMARY KEY (id);

ALTER TABLE ONLY comments
  ADD CONSTRAINT comments_pkey   PRIMARY KEY (id);

ALTER TABLE ONLY reactions
  ADD CONSTRAINT reactions_pkey  PRIMARY KEY (id);

ALTER TABLE ONLY stories
  ADD CONSTRAINT stories_pkey    PRIMARY KEY (id);

---
--- INDEXES
---

CREATE INDEX        ids_type_index
  ON ids      USING BTREE (type);

CREATE UNIQUE INDEX users_username_uindex
  ON users    USING BTREE (username);

CREATE UNIQUE INDEX topics_slug_uindex
  ON topics   USING BTREE (slug);

CREATE INDEX        comments_author_id_index
  ON comments USING BTREE (author_id);

CREATE INDEX        comments_root_id_index
  ON comments USING BTREE (root_id);

CREATE INDEX        comments_parent_id_index
  ON comments USING BTREE (parent_id);

CREATE INDEX        stories_author_id_index
  ON stories  USING BTREE (author_id);

CREATE INDEX        stories_topic_id_index
  ON stories  USING BTREE (topic_id);
