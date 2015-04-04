import pandas as pd
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt
import pylab


bookings = pd.DataFrame(pd.read_csv('bookings.csv', error_bad_lines = False, delimiter = '^'))
searches = pd.DataFrame(pd.read_csv('searches.csv', error_bad_lines = False, delimiter = '^'))

bookings.dtypes
bookings.describe()

# strip out spaces in the column names
bookings.columns = [x.replace(' ','') for x in list(bookings.columns)]
searches.columns = [x.replace(' ','') for x in list(searches.columns)]



### First exercise ###

print "The number of lines in bookings is " + str(bookings.shape[0])
print "The number of lines in searches is " + str(searches.shape[0])

# Results:
# The number of lines in bookings is 10000010
# The number of lines in searches is 20390198


### Second exercise ###
# Top 10 arrival airports in 2013 by number of passengers
bookings2013 = bookings[bookings['year'] == 2013]
Arrport_Pax_2013 = bookings2013[['arr_port','pax']].groupby(['arr_port']).sum()
Top10_Arrport = Arrport_Pax_2013.sort(columns = 'pax', ascending = False).head(10)
print Top10_Arrport

#  Results:
#              pax
#  arr_port       
#  LHR       88809
#  MCO       70930
#  LAX       70530
#  LAS       69630
#  JFK       66270
#  CDG       64490
#  BKK       59460
#  MIA       58150
#  SFO       58000
#  DXB       55590

### Third exercise ###

searches.dtypes
searches.describe()

# select searches for flights arriving at Malaga, Madrid, or Barcelona
MMB_airports = list(['AGP',
                     'MAD',
                     'BCN'])

# need date in month
searches_MMB = searches[searches['Destination'].isin(MMB_airports)][['Date','Destination']]

searches_MMB_pivot = pd.pivot_table(searches_MMB, rows='Date', cols='Destination', aggfunc = np.size)

# need new legend
plt.figure()
searches_MMB_pivot.plot()
pylab.show()








