import cv2
import torch
import numpy as np
from torchvision.transforms import transforms

from bot_gaia.src.models import R2plus1dModel, Mc3Model, R3dModel
from bot_gaia.config import BEST_R2PLUS1_MODEL_PATH, BEST_MC3_MODEL_PATH, BEST_R3D_MODEL_PATH

T1 = 95
T2 = 90
T3 = 80

C = 5
dim = (112, 112)
transformations = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.43216, 0.394666, 0.37645], std=[0.22803, 0.22145, 0.216989])
])


def get_device():
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    return device


def get_coords(frame):
    cframe = frame.copy()

    cframe[cframe[:, :, 2] < 200] = 0
    cframe[cframe[:, :, 0] > 150] = 0
    cframe[cframe[:, :, 1] > 150] = 0
    pos = np.where(cframe != 0)

    x_min = max(0, min(pos[0]) - C)
    x_max = min(cframe.shape[0], max(pos[0]) + C)
    y_min = max(0, min(pos[1]) - C)
    y_max = min(cframe.shape[1], max(pos[1]) + C)

    return x_min, x_max, y_min, y_max


def get_roi(video_file):
    x = []
    video = cv2.VideoCapture(video_file)
    if not video.isOpened():
        print("Error opening video file!")
    first = True
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            if first:
                x_min, x_max, y_min, y_max = get_coords(frame)
                first = False
            crop = frame[x_min:x_max, y_min:y_max, :]
            resized = cv2.resize(crop, dim, interpolation=cv2.INTER_AREA)
            x.append(resized)
        else:
            break
    video.release()
    return x


def write_video(frames, path):
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'avc1'), 15, dim)
    for frame in frames:
        out.write(frame)
    out.release()


def preprocess_frames(frames, device):
    x = [transformations(frame) for frame in frames]
    x = torch.stack(x)
    x = x.permute(1, 0, 2, 3)
    x = x.unsqueeze(0)
    x = x.to(device, dtype=torch.float)
    return x


def load_model_weights(model, model_weights_path, device):
    model.load_state_dict(torch.load(model_weights_path, map_location=device))
    return model


def load_r2plus1d_model(device):
    model = R2plus1dModel().to(device)
    load_model_weights(model, BEST_R2PLUS1_MODEL_PATH, device)
    return model


def load_mc3_model(device):
    model = Mc3Model().to(device)
    load_model_weights(model, BEST_MC3_MODEL_PATH, device)
    return model


def load_r3d_model(device):
    model = R3dModel().to(device)
    load_model_weights(model, BEST_R3D_MODEL_PATH, device)
    return model


def get_model_inference(model, x, threshold):
    with torch.no_grad():
        y = model(x)
        p = y[0].item()
    prob = round(p * 100, 2)
    if prob >= threshold:
        decision = 1
    else:
        decision = 0
        prob = round(100 - prob, 2)
    return decision, prob


def get_ensemble_inference(x, model1, model2, model3):
    decision1, prob1 = get_model_inference(model1, x, T1)
    decision2, prob2 = get_model_inference(model2, x, T2)
    decision3, prob3 = get_model_inference(model3, x, T3)
    if decision1 == decision2 and decision2 == decision3:
        decision = decision1
    elif decision1 == decision2:
        decision = decision1
    elif decision1 == decision3:
        decision = decision1
    elif decision2 == decision3:
        decision = decision2
    return decision
