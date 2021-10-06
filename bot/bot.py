import os
import abc
import time
import json
import logging
import urllib.request
from abc import ABCMeta
from datetime import datetime

from python_wrapper.api import Api
from python_wrapper.status import Status


class Bot(metaclass=ABCMeta):
    def __init__(self, api_version, username, password, email_address, logs_dir, data_dir,
                 start_time=None, duration=None):
        self.api = self._get_api(api_version)
        self.username = username + " " + u"\U0001F916"
        self.password = password
        self.email_address = email_address
        self.start_time = start_time
        self.duration = duration
        self.dataset_completed_by_bot = False
        self.end_time = None
        if self.duration is not None:
            if start_time is not None:
                self.end_time = start_time + duration
            else:
                self.end_time = datetime.now() + duration
            self.stop_condition = lambda: datetime.now() >= self.end_time
        else:
            self.stop_condition = lambda: self.dataset_completed_by_bot
        self.data_dir = data_dir
        self.logs_dir = logs_dir
        self._set_up_logging()
        self._create_data_dir()
        self.movie_path = os.path.join(self.data_dir, "movie.mp4")

    def _get_api(self, api_version):
        api_versions = {
            "dev": "https://dev.stallcatchers.com",
            "prod": "https://stallcatchers.com"
        }
        if api_version not in api_versions.keys():
            raise ValueError("Invalid api version. Expected one of: %s." % api_versions)
        api_host = api_versions[api_version]
        return Api(api_host)

    def _set_up_logging(self):
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        if self.start_time is not None:
            start_time = self.start_time
        else:
            start_time = datetime.now()
        log = os.path.join(self.logs_dir, "{u} {t}.log".format(u=self.username,
                                                               t=start_time.strftime("%d.%m.%Y %H.%M")))
        logging.basicConfig(filename=log, filemode="w", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="%d/%m/%Y %H:%M:%S")

    def _create_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _log_in(self):
        print("\nRegistering bot...")
        register_result = self.api.register(username=self.username, password=self.password, email=self.email_address)
        if register_result == 200:
            print("Done.")
            return False
        elif register_result == 422:
            print("Bot is already registered. Logging in...")
            login_result = self.api.login(username=self.username, password=self.password)
            if login_result is False:
                print("Bad credentials or the bot hasn't been activated.")
                return False
            else:
                print("Successfully logged in.")
                return True

    @abc.abstractmethod
    def _process_movie(self):
        pass

    def _print_score_history(self):
        print("\nGetting score history...")
        score_history = self.api.score_history()
        print(json.dumps(score_history, indent=2))
        print()

    def _process_movies(self):
        if self.start_time is None:
            print("\nStarting now.")
        elif datetime.now() > self.start_time:
            print("\nStart time is in the past.")
            return
        else:
            print("\nWaiting until ", self.start_time, " to begin...")
            while datetime.now() < self.start_time:
                print("\rCurrent time: ", datetime.now().replace(microsecond=0), end="")
                time.sleep(1)
        if self.end_time is not None:
            print("\n\nWill process until ", self.end_time)
        else:
            print("\n\nWill process until the dataset is completed.")
        print("\nBeginning annotations...")
        logging.info("movie_id,num_frames,bot_answer")
        tally = 0
        while not self.stop_condition():
            try:
                if tally % 10 == 0:
                    self._print_score_history()
                movie_json = self.api.movie()
                movie = movie_json["movie"]
                movie_url = movie["urlList"]["movie"]
                movie_id = movie["id"]
                num_frames = movie["numFrames"]
                statuses = movie_json["statuses"]
                if Status.ALL_MOVIES_SEEN_BY_BOT.value in statuses:
                    self.dataset_completed_by_bot = True
                    break
                try:
                    urllib.request.urlretrieve(movie_url, self.movie_path)
                    movie_error = 0
                    bot_answer = self._process_movie()
                except Exception as e:
                    print(e)
                    print(movie_url)
                    movie_error = 1
                    bot_answer = 0
                if bot_answer is not None:
                    self.api.save_movie_answer(movieId=movie_id, answer=bot_answer, movieError=movie_error)
                    logging.info(str(movie_id) + "," + str(num_frames) + "," + str(bot_answer))
                tally += 1
                print(str(tally) + ". " + str(movie_id) + " - " + str(bot_answer))
            except Exception as e:
                print(e)
        self._print_score_history()
        print("Done.")

    def _log_out(self):
        print("\nLogging out...")
        self.api.logout()
        print("Done.")

    def run(self):
        success = self._log_in()
        if success:
            self._process_movies()
            self._log_out()
