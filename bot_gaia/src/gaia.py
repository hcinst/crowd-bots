from bot.bot import Bot
from bot_gaia.src.utils import get_device, load_r2plus1d_model, load_mc3_model, load_r3d_model, get_roi, \
    preprocess_frames, get_ensemble_inference


class Gaia(Bot):
    def __init__(self, api_version, username, password, email_address, logs_dir, data_dir, start_time, duration):
        super(Gaia, self).__init__(api_version, username, password, email_address, logs_dir, data_dir,
                                   start_time, duration)
        self.device = get_device()
        self.model1 = load_r2plus1d_model(self.device)
        self.model2 = load_mc3_model(self.device)
        self.model3 = load_r3d_model(self.device)
        # only on windows
        # import torch
        # torch.set_num_threads(torch.get_num_threads() * 2)
        # torch.set_num_interop_threads(torch.get_num_interop_threads() * 2)

    def _process_movie(self):
        frames = get_roi(self.movie_path)
        if len(frames) > 1:
            x = preprocess_frames(frames, self.device)
            decision = get_ensemble_inference(x, self.model1, self.model2, self.model3)
            return decision
        else:
            return None
