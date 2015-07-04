from urllib2 import Request, urlopen, URLError

import xml.etree.ElementTree as ET
import json
import random
import pickle



#open json file
pictureDict = pickle.load(open("searchResults"))


refinedPictureDict = dict([ (year, pictureDict[year]) for year in pictureDict if int(year) >= yearRange[0] and int(year) < yearRange[1] ])

years = sorted(refinedPictureDict.keys())
print years
#Redefining it for earlier
latest = int(years[-1])
earliest = int(years[0])

gap = (latest-earliest)/(numResults)

earliest = yearRange[0]

toReturn = dict()

#Find them like how we found them before
for i in xrange(numResults):
	#Choose a random list, choose a picture from that
	rList = random.choice([year for year in years if int(year) >= earliest + i*gap and int(year) < earliest+(i+1)*gap  ])
	
	toReturn[str(earliest + i*gap) + "-" + str(earliest + (i+1)*gap)] =  random.choice(pictureDict[rList])

print toReturn
