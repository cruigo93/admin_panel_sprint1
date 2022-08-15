import uuid
from datetime import date, datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField('description', blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
        ]

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'
        indexes = [
            models.Index(fields=['full_name'], name='full_name_idx'),
        ]

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class TypeChoices(models.TextChoices):
        MOVIE = 'MV'
        TV_SHOW = 'TV'
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField('creation_date', blank=True, null=True)
    rating = models.FloatField('rating', blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(100)], null=True)
    type = models.CharField(
        'type', choices=TypeChoices.choices, max_length=255)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    file_path = models.FileField(
        _('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"filmwork"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        indexes = [
            models.Index(fields=['title'], name='title_idx'),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_filmwork"
        indexes = [
            models.Index(fields=['filmwork_id', 'genre_id'],
                         name='filmwork_genre_idx'),
        ]


class PersonFilmwork(UUIDMixin):
    class RoleChoices(models.TextChoices):
        DIRECTOR = 'director', _('director')
        ACTOR = 'actor', _('actor')
        WRITER = 'writer', _('writer')
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), null=True,
                            max_length=255, choices=RoleChoices.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_filmwork"
        indexes = [
            models.Index(fields=['filmwork_id', 'person_id'],
                         name='filmwork_person_idx'),
        ]
