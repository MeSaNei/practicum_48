
-- content_schema.ddl
-- Схема БД для онлайн кинотеатра
-- Автор vpanihin@yandex.ru

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id              uuid PRIMARY KEY,
    title           text NOT NULL,
    description     text,
    creation_date   date,
    rating          double precision,
    type            text NOT NULL,
    created         timestamptz NOT NULL DEFAULT now(),
    modified        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content.genre (
    id          uuid PRIMARY KEY,
    name        text NOT NULL,
    description text,
    created     timestamptz NOT NULL DEFAULT now(),
    modified    timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_genre_name UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS content.person (
    id          uuid PRIMARY KEY,
    full_name   text NOT NULL,
    created     timestamptz NOT NULL DEFAULT now(),
    modified    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id            uuid PRIMARY KEY,
    genre_id      uuid NOT NULL REFERENCES content.genre(id)     ON DELETE CASCADE,
    film_work_id  uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    created       timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_genre_film UNIQUE (film_work_id, genre_id) --одна пара «фильм–жанр» может существовать только один раз.
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id            uuid PRIMARY KEY,
    person_id     uuid NOT NULL REFERENCES content.person(id)    ON DELETE CASCADE,
    film_work_id  uuid NOT NULL REFERENCES content.film_work(id) ON DELETE CASCADE,
    role          text NOT NULL,
    created       timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_person_film_role UNIQUE (film_work_id, person_id, role) --один и тот-же человек не может дублироваться в одной и той-же роли
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_film_work_title           ON content.film_work(title);
CREATE INDEX IF NOT EXISTS idx_film_work_type            ON content.film_work(type);
CREATE INDEX IF NOT EXISTS idx_film_work_creation_date   ON content.film_work(creation_date);

CREATE INDEX IF NOT EXISTS idx_genre_film_work_genre     ON content.genre_film_work(genre_id);
CREATE INDEX IF NOT EXISTS idx_genre_film_work_film      ON content.genre_film_work(film_work_id);

CREATE INDEX IF NOT EXISTS idx_person_film_work_person_role ON content.person_film_work(person_id, role);
CREATE INDEX IF NOT EXISTS idx_person_film_work_film_role   ON content.person_film_work(film_work_id, role);
