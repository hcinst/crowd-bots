from python_wrapper.api import Api

api = Api('https://dev.stallcatchers.com')

# Register the bot in.

register_result = api.register(username='ZFTurbo', password='pass123_turbo', email='zf-turbo@yandex.ru')
print('Reg result: {}'.format(register_result))
if register_result == 422:
    api.login(username='ZFTurbo', password='pass123_turbo')

print(api.movie())

# Request first movie
movie = api.movie()['movie']['id']

# Save movie answer
result = api.save_movie_answer(movieId=movie, answer=1)

# Show result from saving movie ("message received" = success)
print(result)

# Request another movie
print(api.movie())

api.logout()
