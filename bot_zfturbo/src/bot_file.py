from bot.bot import Bot
from bot_zfturbo.src.utils import get_roi, load_zfturbo_model, get_prediction
from classification_models_3D.tfkeras import Classifiers
import time


class ZFTurbo(Bot):
    def __init__(self, api_version, username, password, email_address, logs_dir, data_dir, start_time, duration):
        super(ZFTurbo, self).__init__(api_version, username, password, email_address, logs_dir, data_dir,
                                   start_time, duration)
        self.model = load_zfturbo_model()
        _, self.preproc_input = Classifiers.get('densenet121')

    def _process_movie(self):
        try:
            frames = get_roi(self.movie_path)
            if len(frames) > 1:
                start_time = time.time()
                decision = get_prediction(frames, self.model, self.preproc_input)
                print('Movie: {} Answ: {} Time: {:.2f} sec'.format(self.movie_path, decision, time.time() - start_time))
                return decision
            else:
                return None
        except Exception as e:
            print('Exception: {}'.format(e))
            return None
