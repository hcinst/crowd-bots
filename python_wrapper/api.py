from python_wrapper.http_client import HttpClient


class Api(HttpClient):

    def __init__(self, host):
        """
        Initiate the api connection to this host.

        :param host:
        """
        super(Api, self).__init__(host)

    def register(self, **kwargs):
        """
        Register the bot through api.

        :param kwargs:

        :return:
        """
        response = self.post('/api/register', data=kwargs)
        result = response.json()
        if response.status_code == 200:
            self.access_token = result['token']
        return response.status_code

    def login(self, **kwargs):
        """
        Log the bot in through the api.

        :param kwargs:

        :return:
        """

        try:
            response = self.post('/api/login', data=kwargs).json()
            if "access_token" in response:
                self.access_token = response['access_token']
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def logout(self, **kwargs):
        """
        Log the bot in through the api.

        :param kwargs:

        :return:
        """

        try:
            return self.get('/api/logout', with_access_token=True).json()
        except Exception as e:
            print(e)

    def movie(self):
        """
        Get a random movie.

        :return:
        """
        try:
            return self.get('/api/movie', with_access_token=True).json()
        except Exception as e:
            print(e)

    def save_movie_answer(self, **kwargs):
        """
        Save the movie answer.

        Request body: [movieId, answer]

        :return:
        """
        try:
            return self.post('/api/save-movie-answer', with_access_token=True, data=kwargs).json()
        except Exception as e:
            print(e)

    def score_history(self):
        """
        Retrieve the bot score history.

        :return:
        """

        try:
            return self.get('/api/score-history', with_access_token=True).json()
        except Exception as e:
            print(e)
