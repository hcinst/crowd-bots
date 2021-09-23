# sc-api

## Python wrapper
#### This is a wrapper for the stall catchers bot api.
### Routes

**Register the bot**
<br>
<*host*>/api/register
<br>
Method: POST
<br>
Body: [username, password, email]

**Log the bot in**
<br>
<*host*>/api/login
<br>
Method: POST
<br>
Body: [username, password]

**Log the bot out**
<br>
<*host*>/api/login
<br>
Method: GET
<br>
Body: [username, password]

**Get a movie**
<br>
<*host*>/api/movie
<br>
Method: GET


**Save a movie answer**
<br>
<*host*>/api/save-movie-answer
<br>
Method: POST
<br>
Body: [movieId, answer(1,0)]

**Get score history**
<br>
<*host*>/api/score-history
<br>
Method: GET

## Bot
#### An abstract class for a bot using the api to:
- register
- log in
- process videos
- log out
#### The start time can either be a datetime or None, in which case the bot will start processing right away.
#### The stop condition is controlled using the "duration" argument. The bot will stop either after a set time while there are unseen movies, or if the duration was None, when the active dataset has been completed by the bot. 
#### The only unimplemented method is the one used to process a movie at a time. It should return either 0 or 1, indicating whether the blood vessel section outlined in the video is flowing or stalled.

## Gaia
#### Gaia is an intelligent bot using the 3rd place solution in the Clog Loss competition to make predictions for videos.