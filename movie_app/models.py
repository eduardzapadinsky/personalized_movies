from datetime import date

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class PlaceResidence(models.Model):
    """Місце проживання акторів"""
    country = models.CharField("Країна", max_length=40)
    city = models.CharField("Місто", max_length=40)
    street = models.CharField("Вулиця", max_length=40)
    number = models.CharField("Номер будинку", max_length=10)
    map_coordinate = models.URLField("Координати на мапі", default="https://www.google.com/maps")

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.number}'

    class Meta:
        verbose_name = 'Місце проживання'
        verbose_name_plural = 'Місця проживання'


class Director(models.Model):
    """Режисери"""
    first_name = models.CharField("Ім'я", max_length=100)
    last_name = models.CharField("Прізвище", max_length=100)
    director_email = models.EmailField("Email")
    slug = models.SlugField("Слаг", default='', null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.first_name}-{self.last_name}", allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('director', args=[self.slug])

    class Meta:
        verbose_name = 'Режисер'
        verbose_name_plural = 'Режисери'


class Genre(models.Model):
    """Жанри"""
    name = models.CharField("Жанр", max_length=40)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('genre', args=[self.id])

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Actor(models.Model):
    """Актори"""
    MALE = 'Ч'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Чоловік'),
        (FEMALE, 'Жінка'),
    ]
    first_name = models.CharField("Ім'я", max_length=100)
    last_name = models.CharField("Прізвище", max_length=100)
    gender = models.CharField("Стать", max_length=10, choices=GENDER_CHOICES, default=MALE)
    residence = models.OneToOneField(PlaceResidence, verbose_name="Місце проживання", on_delete=models.SET_NULL,
                                     null=True, blank=True)
    slug = models.SlugField("Слаг", default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.first_name}-{self.last_name}", allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.gender == self.MALE:
            return f'Актор {self.first_name} {self.last_name}'
        else:
            return f'Акторка {self.first_name} {self.last_name}'

    def get_url(self):
        return reverse('actor', args=[self.slug])

    class Meta:
        verbose_name = 'Актор'
        verbose_name_plural = 'Актори'


class Movie(models.Model):
    """Фільми"""

    name = models.CharField("Назва", max_length=50)

    original_name = models.CharField("Англійською", max_length=50)
    # рік випуску
    year = models.IntegerField("Рік", blank=False, validators=[MinValueValidator(1895), MaxValueValidator(2100)])
    # тривалість у хвилинах
    length = models.IntegerField("Тривалість", blank=False, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    genres = models.ManyToManyField(Genre, verbose_name="Жанри", related_name='movies')
    description = models.TextField("Опис", max_length=2000)
    rating_imdb = models.DecimalField("Рейтинг IMDB", max_digits=3, decimal_places=1, validators=[MinValueValidator(0),
                                                                                                  MaxValueValidator(
                                                                                                      10)])
    actors = models.ManyToManyField(Actor, verbose_name="Актори", related_name='movies')
    director = models.ForeignKey(Director, verbose_name="Режисер", on_delete=models.CASCADE, null=True,
                                 related_name='movies')
    slug = models.SlugField("Слаг", default='', null=False)
    picture = models.ImageField("Зображення", upload_to='my_gallery', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.original_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def get_url(self):
        return reverse('movie', args=[self.slug])

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'


class Rating(models.Model):
    """Персональний рейтинг"""
    ip = models.CharField("IP адреса", max_length=15)
    rating = models.DecimalField("Рейтинг", max_digits=3, decimal_places=1, validators=[MinValueValidator(0),
                                                                                        MaxValueValidator(10)])
    viewed_date = models.DateField("Дата останнього перегляду", default=date.today)
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Feedback(models.Model):
    """Відгуки"""
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=20)
    surname = models.CharField("Прізвище", max_length=60)
    feed = models.TextField("Відгук", max_length=5000)
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
