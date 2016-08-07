from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Temp(models.Model):
    movie_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=500)
    year = models.CharField(max_length=6)
    rating = models.FloatField()
    votes = models.IntegerField()
    genre = models.CharField(max_length=500, default='')


    # def __str__(self):
    # 	temp = self.title + ', ' + self.votes ', ' + self.year + ', ' + self.rating + ', ' + self.votes + ', ' + 
    #     return temp

    def __str__(self):
        return self.title

# class Movie(models.Model):
#     title = models.CharField(max_length=30)
#     year = models.CharField(max_length=4)
#     rating = models.CharField(max_length=4)
#     votes = models.CharField(max_length=4)

#     def __str__(self):              # __unicode__ on Python 2
#         return self.title

#     class Meta:
#         ordering = ('title',)

# class Genre(models.Model):
#     name = models.CharField(max_length=100)
#     movies = models.ManyToManyField(Movie)

#     def __str__(self):              # __unicode__ on Python 2
#         return self.name

#     class Meta:
#         ordering = ('name',)