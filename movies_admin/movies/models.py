from django.db import models
import uuid


class Genre(models.Model):
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField('name', max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)
    # auto_now_add автоматически выставит дату создания записи
    created = models.DateTimeField(auto_now_add=True)
    # auto_now изменятся при каждом обновлении записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(models.Model):

    class TypeChoices(models.TextChoices):
        MOVIE = 'MV'
        TV_SHOW = 'TV'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField('creation_date', blank=True)
    rating = models.FloatField('rating', blank=True)
    type = models.CharField(
        'type', choices=TypeChoices.choices, blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"filmwork"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title