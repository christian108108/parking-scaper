#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import re

url = "http://secure.parking.ucf.edu/GarageCount/"

content = urllib2.urlopen(url).read()

soup = BeautifulSoup(content, "lxml")

sAll = soup.findAll("strong")

for garage in sAll:
    spotsLeft = str(garage)
    spotsLeft = int(re.sub('[^0-9]', '', spotsLeft))
    print spotsLeft
