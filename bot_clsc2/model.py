from pathlib import Path

import albumentations as A
import cv2
import numpy as np
import torch

from bot.bot import Bot
from bot_clsc2.config import MODELS_DIR


def get_roi(video_fpath):
    frames = []
    cap = cv2.VideoCapture(video_fpath)
    xs, ys, ws, hs = [], [], [], []
    v_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for _ in range(v_len): 
        _, image = cap.read()
            
        mask = cv2.inRange(image, (9, 13, 104), (98, 143, 255))
        points = np.where(mask > 0)
        p2 = [p for p in zip(points[0], points[1])]
        x, y, w, h = cv2.boundingRect(np.float32(p2))
        xs.append(x)
        ys.append(y)
        ws.append(w)
        hs.append(h)
        frames.append(image[..., -1])

    cap.release()
    
    frames = np.array(frames)
    x = min(xs)
    y = min(ys)
    w = max(ws)
    h = max(hs)

    frames = frames[:, x:x + w, y:y + h]
    frames = np.array(frames).transpose(1, 2, 0)
    
    return frames


def preprocess_frames(frames, fps=2, size=160):
    img = A.Resize(size, size)(image=frames[::fps])['image']
    img = img.astype('float32') / 255
    img = torch.from_numpy(img).permute(2, 0, 1)
    img = img.unsqueeze(0).unsqueeze(0)

    return img


def get_ensemble_inference(x, models, thresh=0.5):
    logits = x.new_zeros((1, 1), dtype=torch.float32)
    for model in models:
        logit = model(x)
        logits += torch.sigmoid(logit)

    logits /= len(models)

    decision = int((logits > thresh).squeeze().item())

    return decision


class CLSC2(Bot):
    def __init__(
            self,
            api_version,
            username,
            password,
            email_address,
            logs_dir,
            data_dir,
            start_time,
            duration,
        ):
        super().__init__(
            api_version,
            username,
            password,
            email_address,
            logs_dir,
            data_dir,
            start_time,
            duration,
        )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = [
            torch.jit.load(str(p), map_location=self.device).eval()
            for p in Path(MODELS_DIR).rglob('*.pt')
        ]
        # only on windows
        # import torch
        # torch.set_num_threads(torch.get_num_threads() * 2)
        # torch.set_num_interop_threads(torch.get_num_interop_threads() * 2)

    def _process_movie(self):
        frames = get_roi(self.movie_path)
        if len(frames) > 1:
            x = preprocess_frames(frames)
            x = x.to(self.device)
            decision = get_ensemble_inference(x, self.models)
        else:
            decision = None

        return decision
