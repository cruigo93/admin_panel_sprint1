from .data import Movie, Genre, Person, PersonFilmwork, GenreFilmwork


class SQLiteLoader:
    def __init__(self, connection) -> None:
        self.connection = connection

    def load_data(self) -> dict[str, list]:
        data = {
            "movies": self.load_movies(),
            "genres": self.load_genres(),
            "persons": self.load_persons(),
            "genre_filmwors": self.load_genre_filmwork(),
            "person_filmwork": self.load_person_filmwork()
        }
        return data

    def load_movies(self) -> list[Movie]:
        curs = self.connection.cursor()
        curs.execute("SELECT * FROM film_work;")
        data = curs.fetchall()
        movies = []
        for m in data:
            movie = Movie(**m)
            movies.append(movie)
        return movies

    def load_genres(self) -> list[Genre]:
        curs = self.connection.cursor()
        curs.execute("SELECT * FROM genre;")
        data = curs.fetchall()
        genres = []
        for g in data:
            genre = Genre(**g)
            genres.append(genre)
        return genres

    def load_persons(self) -> list[Person]:
        curs = self.connection.cursor()
        curs.execute("SELECT * FROM person;")
        data = curs.fetchall()
        persons = []
        for p in data:
            person = Person(**p)
            persons.append(person)
        return persons

    def load_person_filmwork(self) -> list[PersonFilmwork]:
        curs = self.connection.cursor()
        curs.execute("SELECT * FROM person_film_work;")
        data = curs.fetchall()
        records = []
        for p in data:
            pf = PersonFilmwork(**p)
            records.append(pf)
        return records

    def load_genre_filmwork(self) -> list[GenreFilmwork]:
        curs = self.connection.cursor()
        curs.execute("SELECT * FROM genre_film_work;")
        data = curs.fetchall()
        records = []
        for p in data:
            gf = GenreFilmwork(**p)
            records.append(gf)
        return records
