PRAGMA encoding="UTF-8";

CREATE TABLE IF NOT EXISTS user (
    user_id integer primary key,
    first_name text,
    last_name text,
    username text
);

CREATE TABLE IF NOT EXISTS question (
    id integer primary key autoincrement not null,
    question text,
    answer text,
    max_points integer
);

CREATE TABLE IF NOT EXISTS user_question (
    user_id integer not null references user(user_id),
    question_id integer not null references question(id),
    points integer not null
);