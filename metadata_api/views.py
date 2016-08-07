#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.shortcuts import render

from django.http import HttpResponse
from metadata_api.models import Temp
from django.http import JsonResponse
from django.core import serializers
import logging
import json
import codecs
from django.shortcuts import get_object_or_404

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
	""" Get all records from Temp table and return them in a json format.

    Args:
        request: http request..
    Returns:
        HttpResponse json with all records

    """
	datalObj = Temp.objects.all()	
	dataJson = getJsonData(datalObj)

	return HttpResponse(dataJson, content_type="application/json")


def getLatestTitles(request):
	""" Get all titles, order by year descengind.

    Args:
        request: http request..
    Returns:
        HttpResponse json with all records ordered by year.

    """
	datalObj = Temp.objects.all().order_by('-year')
	dataJson = getJsonData(datalObj)
	
	return HttpResponse(dataJson, content_type="application/json")


def getTitleDetails(request, primaryKey):
	""" Get all details for a given title.

    Args:
        request: http request.
        primaryKey: primary key of a title.
    Returns:
        HttpResponse json with all records ordered by year.

    """
	datalObj = Temp.objects.filter(pk=primaryKey)
	dataJson = getJsonData(datalObj)
	
	return HttpResponse(dataJson, content_type="application/json")

def getJsonData(datalObj):
	""" Convert data object from model into json and extract only fields object.

    Args:
        datalObj: model object.
    Returns:
        array of json objects.

    """
	# this produces a list of dictionaries
	dataList = serializers.serialize('python', datalObj)
	
	# extract just the inner `fields` dictionaries since we don't need 'pk' and 'model' values here
	dataFieldsList = [d['fields'] for d in dataList]

	# convert to json and apply indentation so that it's easier to read data
	result = json.dumps(dataFieldsList, sort_keys=True, indent=4)

	return result





