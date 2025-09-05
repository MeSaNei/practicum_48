import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Genre(TimeStampedMixin, UUIDMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField('name', max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name

class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"

class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')

class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('Full name', max_length=255)
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __str__(self):
        return self.full_name 
    
class PersonFilmWork(UUIDMixin):
    class Type(models.TextChoices):
        ACTOR = 'actor', 'Actor'
        DIRECTOR = 'director', 'Director'
        WRITER = 'writer', 'Writer'
        PRODUCER = 'producer', 'Producer'
        COMPOSER = 'composer', 'Composer'
        CINEMATOGRAPHER = 'cinematographer', 'Cinematographer'
        EDITOR = 'editor', 'Editor'
        DESIGNER = 'designer', 'Designer'
        VOICE_ACTOR = 'voice_actor', 'Voice Actor'
    
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    role = models.CharField('role', max_length=50, choices=Type.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work" 
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class FilmWork(TimeStampedMixin, UUIDMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        TV_SHOW = 'tv_show', 'TV Show'

    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    certificate = models.CharField('certificate', max_length=512, blank=True)
    file_path = models.FileField('file', blank=True, null=True, upload_to='movies/')
    creation_date = models.DateField('creation date', blank=True, null=True)
    rating = models.FloatField('rating', blank=True, 
                                validators=[MinValueValidator(0),
                                MaxValueValidator(100)])
    type = models.CharField('type', max_length=50, choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work" 
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title