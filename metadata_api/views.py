#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from metadata_api.models import Temp
from metadata_api.models import Movie
from metadata_api.models import Genre
from metadata_api.models import MovieGenre
import logging
import json
import codecs
import traceback
import sys
import os

def index(request):
	return HttpResponse("Hello! Welcome to the Movie API app!")


def loadData(request):
	""" Load data from text file into a temporary table in the DB.

    Args:
        request: http request.
    Returns:
        HttpResponse    

    """
    # counter for the number of new records that got instereted into DB
	newRecordCouner = 0	

	# open text file with encoding in order to handle foreign characters
	with codecs.open('data/cornell-movie-dialogs-corpus/movie_titles_metadata.txt','r',encoding='utf8') as f:
		# loop through each line of the file
		for line in f:
			line = line.strip('\n')

			# split line into a list by using ' +++$+++ ' delimiter
			splitLine = line.split(" +++$+++ ")

			try: 
				# insert new record into the DB. _ is record object, created is boolean
				_, created = Temp.objects.get_or_create(
			        movie_id=splitLine[0],
			        title=splitLine[1],
			        year=splitLine[2],
			        rating=splitLine[3],
			        votes=splitLine[4],
			        genre=splitLine[5],
			        )

				if created:
					newRecordCouner += 1

			except Exception as e:
				# encode exception error message, just in case there are any non-standard characters, because we're displaying the messsage in HttpResponse
				errorString = unicode(e).encode('utf-8')
				errorMessage = "ERROR:  {0}. Data set: {1}".format(errorString, splitLine)

				return HttpResponse(errorMessage)

	if newRecordCouner > 0:
		resultMessage = 'Inserted {0} new record into the DB'.format(newRecordCouner)
	else:
		resultMessage = 'All movies already exist in the DB, nothing new was inserted.'

	return HttpResponse(resultMessage)


def getAllTitles(request):
	""" Get all records from Movie titles table and return them in a json format.

    Args:
        request: http request..
    Returns:
        HttpResponse json with all records
	
	@todo: convert to load data from joined models: Movie, Genre, MovieGenre
    """
	dataObj = Temp.objects.all()	
	dataJson = getJsonData(dataObj)

	return HttpResponse(dataJson, content_type="application/json")


def getLatestTitles(request):
	""" Get newset 50 titles titles, order by year descending.

    Args:
        request: http request..
    Returns:
        HttpResponse json records result set.

	@todo: convert to load data from joined models: Movie, Genre, MovieGenre
    """
	dataObj = Temp.objects.all().order_by('-year')[:50]
	dataJson = getJsonData(dataObj)
	
	return HttpResponse(dataJson, content_type="application/json")

def getTitlesByYear(request, year):
	""" Get all movie titles from a given year.

    Args:
        request: http request..
        year: year the movie was released
    Returns:
        HttpResponse json records result set.

	@todo: convert to load data from joined models: Movie, Genre, MovieGenre
    """
	dataObj = Temp.objects.filter(year=year)
	dataJson = getJsonData(dataObj)
	
	return HttpResponse(dataJson, content_type="application/json")


def getTitlesByGenre(request, genre):
	""" Get all movie titles with a given genre.

    Args:
        request: http request..
        genre: genre search parameter
    Returns:
        HttpResponse json records result set.

	@todo: convert to load data from joined models: Movie, Genre, MovieGenre
    """
	dataObj = Temp.objects.filter(genre__icontains=genre)
	dataJson = getJsonData(dataObj)
	
	return HttpResponse(dataJson, content_type="application/json")


def getTitleDetails(request, primaryKey):
	""" Get all details for a given title.

    Args:
        request: http request.
        primaryKey: primary key of a title.
    Returns:
        HttpResponse json with all records ordered by year.
	
	@todo: convert to load data from joined models: Movie, Genre, MovieGenre
    """
	movieObj = Temp.objects.filter(pk=primaryKey)
	movieJson = getJsonData(movieObj)
	
	return HttpResponse(movieJson, content_type="application/json")


def getJsonData(dataObj):
	""" Convert data object from model into json and extract only fields object.

    Args:
        dataObj: model object.
    Returns:
        array of json objects.

    """
	# this produces a list of dictionaries
	dataList = serializers.serialize('python', dataObj)
	
	# extract just the inner `fields` dictionaries since we don't need 'pk' and 'model' values here
	dataFieldsList = [d['fields'] for d in dataList]

	# convert to json and apply indentation so that it's easier to read data
	result = json.dumps(dataFieldsList, sort_keys=True, indent=4)

	return result


def migrateRecords(request):
	# counters for the number of new records that got instereted into DB
	newMovieCouner = 0
	newGenreCouner = 0
	newMovieGenreCouner = 0

	# get all records from Temp table in a list format
	records = list(Temp.objects.all())
	
	# loop through each record and then insert into appropriate tables	
	for record in records:
		movieId = record.pk
		genreStr = record.genre.strip('[').strip(']')

		genreList = genreStr.split(', ')
		
		try: 
			for genre in genreList:
				genre = genre.strip("'")

				genreObject, createdGenre = Genre.objects.get_or_create(name=genre)

				genreId = genreObject.pk
				
				if createdGenre:
					newGenreCouner += 1

			movieObject, createdMovie = Movie.objects.get_or_create(
				movie_id=record.movie_id,
				title=record.title,
				year=record.year,
				rating=record.rating,
    			votes=record.votes
				)

			if createdMovie:
				newMovieCouner += 1

			movieGenreObject, createdMovieGenre = MovieGenre.objects.get_or_create(movie_pk=movieObject, genre_pk=genreObject)

			if createdMovieGenre:
				newMovieGenreCouner += 1
		
		except Exception as e:
			tb = traceback.format_exc()

			print("::::: ERROR reported :::::")
			print(tb)
			
			# encode exception error message, just in case there are any non-standard characters, because we're displaying the messsage in HttpResponse
			errorString = unicode(e).encode('utf-8')

			(exc_type, exc_obj, exc_tb) = sys.exc_info()
			excFileName = str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
			excLineNum = str(exc_tb.tb_lineno)
			excType = str(e.__class__.__name__)

			errorMessage = "ERROR: {0}: {1} - {2} (line {3})".format(excType, errorString, excFileName, excLineNum)
			print(errorMessage)

			return HttpResponse(errorMessage)

	resultMessage = "newGenreCouner:  {0}, newMovieGenreCouner: {1}, newMovieGenreCouner: {2}".format(newGenreCouner, newMovieGenreCouner, newMovieGenreCouner)

	return HttpResponse(resultMessage)
