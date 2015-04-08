import pandas as pd
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt
import pylab

bookings = pd.DataFrame(pd.read_csv('bookings.csv', error_bad_lines = False, delimiter = '^'))
searches = pd.DataFrame(pd.read_csv('searches.csv', error_bad_lines = False, delimiter = '^'))


#bookings = pd.DataFrame(pd.read_csv('bookings_sample.csv'))
#searches = pd.DataFrame(pd.read_csv('searches_sample.csv'))

# create variables for matching in Bonus Exercise 1
bookings['booking_date'] = bookings['act_date'].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'))
bookings['boarding_date'] = bookings['brd_time'].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'))
bookings['found_match'] = 0
searches_dedupe['booked'] = 0

"""
Regular data checking and cleaning

"""
bookings.dtypes
searches.dtypes

#strip out spaces
bookings.columns = [x.replace(' ','') for x in list(bookings.columns)]
searches.columns = [x.replace(' ','') for x in list(searches.columns)]

for c in bookings.columns:
    try:
        bookings[c] = [x.strip() for x in bookings[c]]
    except AttributeError:
        print("Didn't make change in ", bookings[c].name)
    
for c in searches.columns:
    try:# deduplicate searches table -- more efficiant calculation
searches_dedupe = searches[-searches.duplicated()]

# create variables for matching
bookings['booking_date'] = bookings['act_date'].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'))
bookings['boarding_date'] = bookings['brd_time'].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d'))
bookings['found_match'] = 0
searches_dedupe['NbSegments'] = searches_dedupe['NbSegments'].astype('int')
searches_dedupe['booked'] = 0
        searches[c] = [x.strip() for x in searches[c]]
    except AttributeError:
        print("Didn't make change in ", searches[c].name)
    
"""
First exercise:

Give number of lines in bookings & searches table

"""

print("The number of lines in bookings is " + str(bookings.shape[0]))
print("The number of lines in searches is " + str(searches.shape[0]))

# Results:
# The number of lines in bookings is 10000010
# The number of lines in searches is 20390198



"""
Second exercise:

Top 10 arrival airports in 2013 by number of passengers

"""

bookings2013 = bookings[bookings['year'] == 2013]
Arrport_Pax_2013 = bookings2013[['arr_port','pax']].groupby(['arr_port']).sum()
Arrport_Pax_2013 = Arrport_Pax_2013.sort(columns = 'pax', ascending = False)
Top10_Arrport = Arrport_Pax_2013.head(10)

print(Top10_Arrport)

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


"""
Third exercise:

Plot the monthly number of searches for flights arriving at Málaga, Madrid or Barcelona.

"""
# select searches for flights arriving at Malaga, Madrid, or Barcelona
MMB_airports = list(['AGP',
                     'MAD',
                     'BCN'])
searches_MMB = searches[searches['Destination'].isin(MMB_airports)][['Date','Destination']]

# get monthly searches data
searches_MMB['Month'] = searches_MMB['Date'].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x, '%Y-%m-%d'), '%Y-%m'))
searches_MMB_pivot = pd.pivot_table(searches_MMB[['Month','Destination']], index='Month', columns='Destination', aggfunc = np.size)
searches_MMB_pivot.columns = ['Malaga', 'Madrid', 'Barcelona']

# Plot
plt.figure()
plt_searches = searches_MMB_pivot.plot(title = 'Searches by Month')
plt_searches.set_ylabel('Total Searches')
pylab.show()


"""
Bonus exercise 1

Match searches with bookings, mark booked searches in the searches table


    Matching criteria:
    A search is booked if
    1. all its segments has a corresponding booking record
       with matched Dep & Arr port, boarding date
    2. The search date is on the same day of the booking date

    Assumptions:
    1. Identical rows in searches are from same end-user
    2. Identical rows in bookings are from different end-users
    
"""


# deduplicate searches table -- more efficiant calculation
searches_dedupe = searches[-searches.duplicated()]

# define a function that find a matching recording in bookings table
# if a booking record was already used to match another search, it cannot be reused
def FindFirstMatch(segment_matches):
    match_id = np.nan
    for i in range(bookings.shape[0]):
        if segment_matches['matched'].ix[i] and bookings['found_match'].ix[i] == 0:
            match_id = i
            break
    return match_id

# define a function to single out segments in a search record, and organize them in SegmentInfoTable table
def GetSegmentInfo(NbSeg, s):
    SegmentInfoTable = pd.DataFrame()
    for i in range(1,int(NbSeg+1)):
        SegDeparture = str('Seg') + str(i) + str('Departure')
        SegArrival = str('Seg') + str(i) + str('Arrival')
        SegDate = str('Seg') + str(i) + str('Date')
        SearchDate = str('Date')
        SegmentInfo = [x for x in searches_dedupe[[SegDeparture,SegArrival,SegDate,SearchDate]].iloc[s]]
        SegmentInfoTable[str('Segment') + str(i)] = SegmentInfo
    return SegmentInfoTable

# define a function to get the index of the bookings that matches a search,
# if a search contains a number of segments, it will regenerate a list of indexes that match those segments
def GetSegmentMatchID(NbSeg, SegmentInfoTable):
    MatchID = list()
    Booking_info = list(['dep_port','arr_port','boarding_date','booking_date'])
    for i in range(1, int(NbSeg+1)):
        segment_info = SegmentInfoTable[str('Segment') + str(i)]
        segment_matches = bookings[Booking_info].isin(segment_info)
        segment_matches['matched'] = segment_matches.apply(np.all, axis = 1)
        match_id = FindFirstMatch(segment_matches)
        MatchID.append(match_id)
    return MatchID

# define a function to mark the valid matches in the bookings and searches table
def MarkMatches(s, NbSeg, MatchID):
    NbMatches = len(MatchID) - sum(np.isnan(MatchID))
    if NbSeg == NbMatches:
        searches_dedupe['booked'].ix[s] = 1        
        bookings['found_match'].ix[MatchID] = 1    
        
# loop through the searches table to match the bookings table, and generate a field with 1 as booked, 0 not booked 
for s in searches_dedupe.index:
    NbSeg = searches['NbSegments'].ix[s]
    SegmentInfoTable = GetSegmentInfo(NbSeg,s)
    MatchID = GetSegmentMatchID(NbSeg, SegmentInfoTable)
    MarkMatches(s, NbSeg, MatchID)

#Join deduped searches with original searches
pd.merge(searches, searches_dedupe, on = list(searches.columns), how = 'left')
searches.to_csv("searches_booked.csv")

