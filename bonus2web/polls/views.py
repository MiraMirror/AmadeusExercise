from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt
import pylab

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, n):

	##bookings = pd.DataFrame(pd.read_csv('bookings.csv', error_bad_lines = False, delimiter = '^'))


	bookings = pd.DataFrame(pd.read_csv('bookings_sample.csv'))
	bookings.columns = [x.replace(' ','') for x in list(bookings.columns)]

	### Second exercise ###
	# Top N arrival airports in 2013 by number of passengers
	parameter = int(n)
	bookings2013 = bookings[bookings['year'] == 2013]
	Arrport_Pax_2013 = bookings2013[['arr_port','pax']].groupby(['arr_port']).sum()
	Arrport_Pax_2013 = Arrport_Pax_2013.sort(columns = 'pax', ascending = False)
	TopN_Arrport = Arrport_Pax_2013.head(parameter)
	
	TopN_Arrport.to_json("TopN_Arrport.json")

	response_string = "Success! The top {0} arriving airports are in your folder!".format(parameter)

	if parameter > 0: 
		return HttpResponse(response_string)
	else:
		return HttpResponse("You must enter a rank greater than 0.")
	"""
	Wrap the output of the second exercise in a web service that returns the data in 
	JSON format (instead of printing to the standard output). The web service should
	accept a parameter n>0. For the top 10 airports, n is 10. For the X top airports, n is X.
	
	"""
