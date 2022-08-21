import os
from contextlib import contextmanager

from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
import psycopg2
import sqlite3

from dotenv import load_dotenv

from loading import PostgresSaver, SQLiteLoader
from loading.data import Movie, Person, Genre, PersonFilmwork, GenreFilmwork


load_dotenv()

CONFIG = {
    "POSTGRES_DBNAME": os.environ.get('POSTGRES_DBNAME'),
    "POSTGRES_USER": os.environ.get('POSTGRES_USER'),
    "POSTGRES_PASS": os.environ.get('POSTGRES_PASS'),
    "POSTGRES_HOST": os.environ.get('POSTGRES_HOST'),
    "POSTGRES_PORT": os.environ.get('POSTGRES_PORT'),

    "SQLITE_PATH": os.path.join(os.getcwd(), os.environ.get('SQLITE_PATH')),
}


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def pg_conn_context(dsl: dict):
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield pg_conn
    pg_conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    for data in sqlite_loader.load(Movie, 'film_work'):
        postgres_saver.save_all_filmworks(data)
    for data in sqlite_loader.load(Genre, 'genre'):
        postgres_saver.save_all_genres(data)
    for data in sqlite_loader.load(Person, 'person'):
        postgres_saver.save_all_persons(data)
    for data in sqlite_loader.load(GenreFilmwork, 'genre_film_work'):
        postgres_saver.save_all_genre_filmworks(data)
    for data in sqlite_loader.load(PersonFilmwork, 'person_film_work'):
        postgres_saver.save_all_person_filmworks(data)


if __name__ == '__main__':
    dsl = {'dbname': CONFIG['POSTGRES_DBNAME'], 'user': CONFIG['POSTGRES_USER'],
           'password': CONFIG['POSTGRES_PASS'], 'host': CONFIG['POSTGRES_HOST'], 'port': CONFIG['POSTGRES_PORT']}
    with conn_context(CONFIG['SQLITE_PATH']) as sqlite_conn, pg_conn_context(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
