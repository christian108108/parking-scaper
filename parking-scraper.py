#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import re


def printGarage(garage):
    if garage == "Libra":
        print "Libra Garage:  ", dictionary[garage]
    else:
        print "Garage ", garage, ": \t", dictionary[garage]


url = "http://secure.parking.ucf.edu/GarageCount/"

garages = ["A", "B", "C", "D", "H", "I", "Libra"]
spots = []

content = urllib2.urlopen(url).read()

soup = BeautifulSoup(content, "lxml")

tags = soup.findAll("strong")

for x in tags:
    currentSpot = str(x)
    currentSpot = int(re.sub('[^0-9]', '', currentSpot))
    spots.append(currentSpot)


dictionary = dict(zip(garages, spots))


print "Spots available"
for garage in sorted(dictionary):
    printGarage(garage)
