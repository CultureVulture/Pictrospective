from urllib2 import Request, urlopen, URLError

import xml.etree.ElementTree as ET
import json
import random
import pickle


import SimpleHTTPServer
import SocketServer

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
			self.path = '/index.html'
		elif self.path == '/search':
			urlparts = urlparse.urlpase(self.path)
			return search(urlparts.params['search'])
		#return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def search(term):
	#Finds numPictures of data and return numResults that are spaced evenly
	term = term.replace(" ", "%20")

	search = "http://api.trove.nla.gov.au/result?key=qfmfb53vlncd3s1q&zone=picture&n=100&l-format=Photograph&q=" + term
	currentSearch = search
	troveBase = "http://trove.nla.gov.au"

	#key = qfmfb53vlncd3s1q
	numPictures = 20
	s = 0
	size = 0
	while True:
		try:
			response = urlopen(currentSearch)
		except URLError, e:
			print 'Not valid URL', e
			break
			
			
		pictureTree = ET.parse(response)

		response.close()

		pictureDict = dict()
		picturePictures = pictureTree.findall(".//work")

		for picture in picturePictures:

			id = str(picture.attrib["id"])
			troveLink = picture.attrib["url"]

			#Only want Photos
			if picture.find("type").text != "Photograph":
				continue
			#Find the year made, only want images with a year
			try:
				year = picture.find("issued").text
				try:
					if int(year) > 2015:
						continue
				except:
					continue
			except AttributeError:
				continue

			#Find name and caption
			name = picture.find("title").text
			try:
				caption = picture.find("snippet").text
			except AttributeError:
				caption = ""

			#Get fulltext original link
			for ident in picture.iter("identifier"):
				if ident.attrib["linktype"] == "fulltext":
					resource = ident.text
				elif ident.attrib["linktype"] == "thumbnail":
					thumbImage = ident.text
					image = ""
					if thumbImage[-5] == "t" and "acms.sl.nsw.gov.au" in image:
						image = thumbImage[:-5] + "r.jpg" 

			try:
				pictureDict[year].append( dict() )
			except:
				pictureDict[year] = [ dict() ]

			#pictureDict[year][-1]["name"] = name
			pictureDict[year][-1]["year"] = year
			#pictureDict[year][-1]["caption"] = caption
			pictureDict[year][-1]["troveLink"] = troveBase + troveLink
			pictureDict[year][-1]["link"] = resource
			pictureDict[year][-1]["thumbnail"] = thumbImage
			pictureDict[year][-1]["image"] = image
		

			size += 1

		if size > numPictures:
			break
		#Get the next results
		s += 100
		currentSearch = search + "&s=" +str(s)

	#Find earliest and latext year picture
	years = sorted(pictureDict.keys())

	earliest = int(years[0])

	latest = int(years[-1])

	#Rounded to nearest decade
	gap = ((latest-earliest)/(numResults) + 10)/10*10

	#Round earliest to nearest decade: Yay for integer arithmetic
	earliest = earliest /10 * 10

	print earliest, latest, gap
	toReturn = dict()

	for i in xrange(numResults):
		#Choose a random list, choose a picture from that
		rList = random.choice([year for year in years if int(year) >= earliest + i*gap and int(year) < earliest+(i+1)*gap  ])
		toReturn[str(earliest + i*gap) + "-" + str(earliest + (i+1)*gap)] =  random.choice(pictureDict[rList])

	#Save results for later looking into
	pickle.dump(pictureDict, open('searchResults', 'wb'))

	return json.dumps(toReturn)


Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)

server.serve_forever()