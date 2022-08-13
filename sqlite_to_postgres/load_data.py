from loading import PostgresSaver, SQLiteLoader
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
import psycopg2
import sqlite3
import os
from contextlib import contextmanager
from dotenv import load_dotenv
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
    yield conn  # С конструкцией yield вы познакомитесь в следующем модуле
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_data()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': CONFIG['POSTGRES_DBNAME'], 'user': CONFIG['POSTGRES_USER'],
           'password': CONFIG['POSTGRES_PASS'], 'host': CONFIG['POSTGRES_HOST'], 'port': CONFIG['POSTGRES_PORT']}
    with conn_context(CONFIG['SQLITE_PATH']) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
