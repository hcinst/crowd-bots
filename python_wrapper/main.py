from api import Api

api = Api('https://dev.stallcatchers.com')

# Register the bot in.

register_result = api.register(username='', password='', email='')
if register_result == 422:
    api.login(username='', password='')

# Request first movie
movie = api.movie()['movie']['id']

# Save movie answer
result = api.save_movie_answer(movieId=movie, answer=1)

# Show result from saving movie ("message received" = success)
print(result)

# Request another movie
print(api.movie())

api.logout()
