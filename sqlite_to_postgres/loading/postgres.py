from .data import Movie, Genre, Person, PersonFilmwork, GenreFilmwork
import uuid
from psycopg2.extras import execute_batch
from datetime import date, datetime


class PostgresSaver:
    def __init__(self, pg_conn) -> None:
        self.pg_conn = pg_conn

    def save_all_persons(self, data: list, n: int = 16) -> None:
        with self.pg_conn.cursor() as cur:
            query = 'INSERT INTO content.person (id, full_name, created, modified) \
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING; '
            insert_data = [(p.id, p.full_name, p.created_at, datetime.now())
                           for p in data]
            execute_batch(cur, query, insert_data, page_size=n)
            self.pg_conn.commit()

    def save_all_filmworks(self, data: list, n: int = 16) -> None:
        with self.pg_conn.cursor() as cur:
            query = 'INSERT INTO content.filmwork (id, title, created, modified, description, creation_date, rating, type) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING; '
            insert_data = [(m.id, m.title, m.created_at, datetime.now(), m.description, m.creation_date, m.rating, m.type)
                           for m in data]
            execute_batch(cur, query, insert_data, page_size=n)
            self.pg_conn.commit()

    def save_all_genres(self, data: list, n: int = 16) -> None:
        with self.pg_conn.cursor() as cur:
            query = 'INSERT INTO content.genre (id, name, description, created, modified) \
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING; '
            insert_data = [(g.id, g.name, g.description, g.created_at, datetime.now())
                           for g in data]
            execute_batch(cur, query, insert_data, page_size=n)
            self.pg_conn.commit()

    def save_all_genre_filmworks(self, data: list, n: int = 16) -> None:
        with self.pg_conn.cursor() as cur:
            query = 'INSERT INTO content.genre_filmwork (id, genre_id, filmwork_id, created) \
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING; '
            insert_data = [(g.id, g.genre_id, g.film_work_id, datetime.now())
                           for g in data]
            execute_batch(cur, query, insert_data, page_size=n)
            self.pg_conn.commit()

    def save_all_person_filmworks(self, data: list, n: int = 16) -> None:
        with self.pg_conn.cursor() as cur:
            query = 'INSERT INTO content.person_filmwork (id, person_id, filmwork_id, role, created) \
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING; '
            insert_data = [(p.id, p.person_id, p.film_work_id, p.role,
                            datetime.now()) for p in data]
            execute_batch(cur, query, insert_data, page_size=n)
            self.pg_conn.commit()
