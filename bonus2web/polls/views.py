from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt
import pylab

def index(request):
    return HttpResponse("Hello, you can extract top N arriving airports searches from here!")

def detail(request, n):

	parameter = int(n)
	Arrport_Pax_2013 = pd.DataFrame(pd.read_csv("Ex2_arrportbypax.csv"))
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
