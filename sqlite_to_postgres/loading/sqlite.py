from .data import Movie, Genre, Person, PersonFilmwork, GenreFilmwork


class SQLiteLoader:
    def __init__(self, connection) -> None:
        self.connection = connection

    # def load_data(self) -> dict[str, list]:
    #     data = {
    #         "movies": self.load_(Movie, 'film_work'),
    #         "genres": self.load_(Genre, 'genre'),
    #         "persons": self.load_(Person, 'person'),
    #         "genre_filmwors": self.load_(GenreFilmwork, 'genre_film_work'),
    #         "person_filmwork": self.load_(PersonFilmwork, 'person_film_work')
    #     }
    #     return data

    def load(self, data_class, table_name: str, batch_size: int = 100) -> list[Movie]:
        curs = self.connection.cursor()
        curs.execute(f"SELECT * FROM {table_name};")

        while True:
            data = curs.fetchmany(batch_size)
            if not data:
                break
            records = []
            for m in data:
                record = data_class(**m)
                records.append(record)
            yield records
