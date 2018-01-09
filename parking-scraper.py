#!/usr/bin/python

from bs4 import BeautifulSoup
from twython import Twython
import urllib2
import re

def printGarage(garage):
    if garage == "Libra":
        textArray.append("Libra Garage: " + str(dictionary[garage]))
    else:
        textArray.append("Garage " + garage + ": " + str(dictionary[garage]))

def initializeBeautifulSoup():
    url = "http://secure.parking.ucf.edu/GarageCount/"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    #find the tags that say "strong" which are only the number of spaces available
    #should look like "<strong>123</strong>"
    tags = soup.findAll("strong")

    #loops through each "<strong>123</strong>" tag from BeautifulSoup
    for x in tags:
        currentSpot = str(x)
        currentSpot = int(re.sub('[^0-9]', '', currentSpot))
        spots.append(currentSpot)

def arrayToString(array):
    #converts array into string and adds newline after each line except the final
    myString = ""
    for line in array[:-1]:
        myString += str(line)
        myString += "\n"
    myString += str(array[-1])

    return myString

def initializeTwython():
    APP_KEY = 'REDACTED'
    APP_SECRET = 'REDACTED'
    OAUTH_TOKEN = 'REDACTED'
    OAUTH_TOKEN_SECRET = 'REDACTED'

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    auth = twitter.get_authentication_tokens()

    return twitter

def tweet(twitter, tweetString):
    twitter.update_status(status=tweetString)

#makes two lists: one for garage names, another empty list for the spots of each garage
garages = ["A", "B", "C", "D", "H", "I", "Libra"]
spots = []

#initialize BeautifulSoup and get tags that look like "<strong>123</strong>"
initializeBeautifulSoup()

#matches number of spots to the garage in a dictionary instead of two seperate lists
dictionary = dict(zip(garages, spots))

#Creates empty array to later construct one big string
textArray = []
textArray.append("Spots available")

#loops through each garage in the dictionary and prints out each one
for garage in sorted(dictionary):
    printGarage(garage)

#converts array "s" into a big string ready to tweet
tweetString = arrayToString(textArray)

print tweetString

twitter = initializeTwython()

#Tweet!
tweet(twitter, tweetString)
