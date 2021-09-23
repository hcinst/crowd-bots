# KAOS - the randomly responding Catcher Bot ("cbot")  that can play Stall Catchers (stallcatchers.com)
# Copyright 2021 Human Computation Institute
# Creative Commons License: CC-BY-SA 4.0
# This example cbot was created by Pietro Michelucci and named by Laura Onac
# NOTE: you must set the START_TIME below before running this example.

import logging
import time
from datetime import datetime
from datetime import timedelta
from random import randint
from api import Api

# Create API object setting location of Stall Catchers
# (use dev.stallcatchers.com for testing, and stallcatchers.com for production)
api = Api('https://dev.stallcatchers.com')

# Constant declarations
USERNAME = ''
PASSWORD = ''
START_TIME = datetime(2021, 4, 14, 18, 20, 0, 0)
DURATION = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1,
                     weeks=0)  # continue requesting movies for this duration

# Set up logging
log = "cbot.log"
logging.basicConfig(filename=log, filemode="w", level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')

# Calculate end time
end_time = START_TIME + DURATION

# Register bot
print('registering bot')
register_result = api.register(username=USERNAME, password=PASSWORD, email='hchandbook+kaos@gmail.com')

# If bot is already registered (error 422) then just login
print('bot already registered - logging in')
if register_result == 422:
    api.login(username=USERNAME, password=PASSWORD)

# save header fields to log file
print('initializing log file')
logging.info('movie_url,movie_id,num_frames,cbot_answer,save_message')

print('waiting until ', START_TIME, ' to begin...')

# wait until start time to begin requesting movies
while datetime.now() < START_TIME:
    print('\rcurrent time: ', datetime.now().replace(microsecond=0), end='')
    time.sleep(1)  # wait one second and try again

print('')
print('will annotate until ', end_time.replace(microsecond=0))
print('beginning annotations')

# set classification counter at zero
tally = 0

# continue requesting movies until reaching the end time
while datetime.now() < end_time:
    movie_json = api.movie()  # request new movie and retrieve json record with new movie info
    movie_url = movie_json['movie']['urlList']['movie']  # extract movie URL from json
    movie_id = movie_json['movie']['id']  # extract movie id from json
    num_frames = movie_json['movie']['numFrames']  # extract number of frames in movie from json
    cbot_answer = randint(0, 1)  # bot computes answer - 0=flowing, 1=stalled
    time.sleep(1)  # wait one second before answering, otherwise it will generate error 429 (too many requests)
    save_result = api.save_movie_answer(movieId=movie_id, answer=cbot_answer)
    tally += 1
    logging.info(movie_url + ',' + str(movie_id) + ',' + str(num_frames) + ',' + str(cbot_answer) + ',', save_result)
    print(str(tally) + ': ' + str(movie_id))  # console output to count movies annotated and show each movie id
    time.sleep(1)  # wait one second before answering, otherwise it will generate error 429 (too many requests)

print('finished annotating')

# cbot logs out
api.logout()

print('logged out')
