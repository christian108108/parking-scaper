#!/usr/bin/python

from parking_scraper import *


#scrape the website for parking spots
soup = generate_soup()

#populates the garage list
garage_list = populate_garage_list(soup)

#prepare the public tweet
message = prepare_public_tweet(garage_list)

twitter = initialize_twython()

tweet(twitter, message)
