#!/usr/bin/python

import googlemaps
import string
from bs4 import BeautifulSoup
import urllib2
import re
import json
from twython import Twython


class Garage:

    def __init__(self, name, spots, coordinates):
        self.name = name
        self.spots = spots
        self.coordinates = coordinates

    def __repr__(self):
        if(self.name == "Libra"):
            return "%s Garage" % (self.name)
        else:
            return "Garage %s" % (self.name)

class Building:

    def __init__(self, name, abbreviation, coordinates):
        self.name = name
        self.abbreviation = abbreviation
        self.coordinates = coordinates

    def __repr__(self):
        return "%s" % (self.abbreviation)

    def get_directions(self, garage, gmaps):
        #uses Google API to fetch the walking directions from the input garage to the building
        directions_result = gmaps.directions(garage.coordinates, self.coordinates, mode="walking")
        #fetches the string that says "9 min" or something like that
        directions_result = str(directions_result[0]['legs'][0]['duration']['text'])

        #returns output like "9 mins" or "4 h 23 mins"
        return directions_result


def generate_soup():
    url = "http://secure.parking.ucf.edu/GarageCount/"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")

    return soup

def soup_to_list(soup):

    #only takes the tags with <strong>123</strong>
    tags = soup.findAll("strong")

    #creates empty list of spots per garage
    spots_per_garage_list = []

    #loops through each "<strong>123</strong>" tag from BeautifulSoup
    for x in tags:
        spots = str(x)
        spots = int(re.sub('[^0-9]', '', spots))
        #appends each raw number (123) into the list
        spots_per_garage_list.append(spots)

    #returns list [123, 456, 789]
    return spots_per_garage_list

def is_valid_item(item):
    #if there are coordinates and there's an abbreviation code for it
    return (type(item.get("googlemap_point")) is list) and (item.get("abbreviation") is not None)

def search_building_list(building_list, input_name):
    #search building list for the one the user wants to navigate to
    for building in building_list:
        #if the name or abbreviation match, then return the coordinates
        if (building.name.upper() == input_name) or (building.abbreviation == input_name):
            return building

    #if it can't find the building, return None
    return None

def populate_building_list():
    #opens locations.json file and stores it as variable d
    with open('locations.json') as json_data:
        d = json.load(json_data)

    building_list = []
    #iterate through the json data "d" and each structure is called "item"
    for item in d:
        #if the current structure is valid (has coordinates AND an abbreviation)
        if(is_valid_item(item)):
            #adds a new building from the JSON file to the list of buildings
            building = Building(item.get("name"), item.get("abbreviation"), re.sub('[\[\]]', '', str(item.get("googlemap_point"))))
            building_list.append(building)

    return building_list

def populate_garage_list(soup):
    #makes lists of garage names
    garage_name_list = ['A','B','C','D','H','I','Libra']
    #creates list of spots per garage
    spots_per_garage_list = soup_to_list(soup)
    #creates list of each garage's coordinates
    garage_coordinate_list = ["28.599857, -81.205603","28.596944, -81.200448","28.602405, -81.197180","28.604928, -81.197191",
                              "28.604996, -81.201221","28.601118, -81.204828","28.595997, -81.196697"]
    #makes empty garage list
    garage_list = []

    #takes values from each parking garage and makes a list of Garage objects with proper attributes
    for name, spots, coordinates in zip(garage_name_list, spots_per_garage_list, garage_coordinate_list):
        #adds to the list
        garage_list.append(Garage(name, spots, coordinates))

    return garage_list

def prepare_public_tweet(garage_list):
    #prepares a string to tweet to the public
    message = "Spots available\n"

    for garage in garage_list[:-1]:
        message += "%s: %d\n" % (garage, garage.spots)

    #prints the last line without the \n character
    message += "%s: %d" % (garage_list[-1], garage_list[-1].spots)

    return message

def prepare_direct_message(building, garage_list, gmaps):
    #prepares a string to send in a direct message
    message = ""

    #if the building is not found, then just return the generic public tweet with a help message
    if building is None:
        return "%s\n\nFor a list of building codes, go to map.ucf.edu/locations" % prepare_public_tweet(garage_list)

    #iterates through each garage in the list
    for garage in garage_list[:-1]:
        #grabs walking distance from garage x, building short code (ex. MSB), garage name (ex. Garage D), and spots left
        #adds to the final message
        message += "%s to %s: %s walk. %d spots free\n" % (garage, building.abbreviation, building.get_directions(garage, gmaps), garage.spots)

    #prints the last line to treat it differently (no \n chararacter)
    message += "%s to %s: %s walk. %d spots free" % (garage_list[-1], building.abbreviation, building.get_directions(garage_list[-1], gmaps), garage_list[-1].spots)

    return message

def initialize_twython():

    APP_KEY = ''
    APP_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''


    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    auth = twitter.get_authentication_tokens()

    return twitter

def tweet(twitter, tweetString):
    twitter.update_status(status=tweetString)

def initialize_google_maps():
    return googlemaps.Client(key='')
