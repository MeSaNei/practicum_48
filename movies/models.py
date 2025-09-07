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
    name = models.CharField(_('Name'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
    
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
    full_name = models.CharField(_('Full name'), max_length=255)
    gender = models.TextField(_('Gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Man')
        verbose_name_plural = _('Men')

    def __str__(self):
        return self.full_name 
    
class PersonFilmWork(UUIDMixin):
    class Type(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        DIRECTOR = 'director', _('Director')
        WRITER = 'writer', _('Writer')
        PRODUCER = 'producer', _('Producer')
        COMPOSER = 'composer', _('Composer')
        CINEMATOGRAPHER = 'cinematographer', _('Cinematographer')
        EDITOR = 'editor', _('Editor')
        DESIGNER = 'designer', _('Designer')
        VOICE_ACTOR = 'voice_actor', _('Voice Actor')
    
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    role = models.CharField(_('Role'), max_length=50, choices=Type.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work" 
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


class FilmWork(TimeStampedMixin, UUIDMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    certificate = models.CharField(_('Certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('File'), blank=True, null=True, upload_to='movies/')
    creation_date = models.DateField(_('Creation date'), blank=True, null=True)
    rating = models.FloatField(_('Rating'), blank=True, 
                                validators=[MinValueValidator(0),
                                MaxValueValidator(100)])
    type = models.CharField(_('Type'), max_length=50, choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"film_work" 
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')

    def __str__(self):
        return self.title