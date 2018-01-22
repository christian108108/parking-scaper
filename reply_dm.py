#!/usr/bin/python

from parking_scraper import *

#scrape the website for parking spots
soup = generate_soup()

#populates the garage list
garage_list = populate_garage_list(soup)

#populates the building list
building_list = populate_building_list()

#initializes Google Maps API to get directions from each garage to a given building
gmaps = initialize_google_maps()

#initializes Twitter API in order to grab direct messages from users
twitter = initialize_twython()

#grabs the list of direct messages
message_list = twitter.get_direct_messages()

#grabs the most recent message
newest_message = message_list[0]

destination_building = search_building_list(building_list, input_name=newest_message['text'])
message = prepare_direct_message(destination_building, garage_list, gmaps)

twitter.send_direct_message(user_id=newest_message['sender']['id'], text=message)


#prepare the direct message
#message = prepare_direct_message(garage_list)
