from __future__ import unicode_literals
from django.db import models


class Temp(models.Model):
    """ Temp model. Tempapry place to store all movies and genres in one table.
    """
    movie_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=500)
    year = models.CharField(max_length=6)
    rating = models.FloatField()
    votes = models.IntegerField()
    genre = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.title


class Movie(models.Model):
    """ Movies model
    """
    movie_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=500)
    year = models.CharField(max_length=6)
    rating = models.FloatField()
    votes = models.IntegerField()

    def __str__(self):
        return self.title


class Genre(models.Model):
    """ Genre model
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='')

    class Meta:
        ordering = ('name',)


class MovieGenre(models.Model):
    """ Movie-Genre model. Relationship table between Movie and Genre.
    """
    movie_pk = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre_pk = models.ForeignKey(Genre, on_delete=models.CASCADE)
