-- create schema
CREATE SCHEMA IF NOT EXISTS content;

-- create table
CREATE TABLE IF NOT EXISTS content.filmwork (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_filmwork (
    id uuid PRIMARY KEY,
    filmwork_id uuid NOT NULL REFERENCES content.filmwork (id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.genre_filmwork (
    id uuid PRIMARY KEY,
    filmwork_id uuid NOT NULL REFERENCES content.filmwork (id) ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    created timestamp with time zone
); 

CREATE UNIQUE INDEX person_filmwork_role_idx on content.person_filmwork(filmwork_id, person_id, role);
CREATE UNIQUE INDEX genre_filmwork_idx on content.genre_filmwork(filmwork_id, genre_id);

