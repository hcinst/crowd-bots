if __name__ == '__main__':
    import os

    gpu_use = 4
    print('GPU use: {}'.format(gpu_use))
    os.environ["KERAS_BACKEND"] = "tensorflow"
    os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(gpu_use)
    

import cv2
import numpy as np
import os
import time
from tensorflow.keras.models import load_model
from volumentations import *
from classification_models_3D.tfkeras import Classifiers
from bot_zfturbo.config import BEST_MODEL_PATH, TEST_VIDEO


SHAPE_SIZE = (96, 128, 128, 3)
THR_FOR_MCC = 0.7


def get_roi(video_file):
    cap = cv2.VideoCapture(video_file)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    frame_list = []
    print('ID: {} Video length: {}'.format(os.path.basename(video_file), length))
    min_x = 10000000
    min_y = 10000000
    max_x = -10000000
    max_y = -10000000
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret is False:
            break
        th = cv2.inRange(frame, (9, 13, 104), (98, 143, 255))
        points = np.where(th > 0)
        p2 = zip(points[0], points[1])
        p2 = [p for p in p2]
        rect = cv2.boundingRect(np.float32(p2))
        frame_list.append(frame.copy())
        if rect[1] < min_x:
            min_x = rect[1]
        if rect[0] < min_y:
            min_y = rect[0]
        if rect[1] + rect[3] > max_x:
            max_x = rect[1] + rect[3]
        if rect[0] + rect[2] > max_y:
            max_y = rect[0] + rect[2]

    frames = np.array(frame_list, dtype=np.uint8)
    frames = frames[:, min_y:max_y, min_x:max_x, :]
    cap.release()
    return frames


def load_zfturbo_model():
    model = load_model(BEST_MODEL_PATH)
    print(model.summary())
    return model


def get_augmentation_valid(patch_size):
    return Compose([
        Resize(patch_size, interpolation=1, always_apply=True, p=1.0),
    ], p=1.0)


def get_cube_pred_v2(model, cube, preproc_input):
    valid_aug = get_augmentation_valid(SHAPE_SIZE[:3])
    data = {'image': cube}
    aug_data = valid_aug(**data)
    cube = aug_data['image']

    cubes_to_pred = []
    for i in range(8):
        cout = np.zeros(SHAPE_SIZE, dtype=np.uint8)
        if i == 0:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube.copy()
        elif i == 1:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[::-1, :, :].copy()
        elif i == 2:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[:, ::-1, :].copy()
        elif i == 3:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[:, :, ::-1].copy()
        elif i == 4:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[::-1, ::-1, :].copy()
        elif i == 5:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[:, ::-1, ::-1].copy()
        elif i == 6:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[::-1, :, ::-1].copy()
        elif i == 7:
            cout[:cube.shape[0], :cube.shape[1], :cube.shape[2], :cube.shape[3]] = cube[::-1, ::-1, ::-1].copy()
        cubes_to_pred.append(cout.copy())

    cubes = np.array(cubes_to_pred)
    cubes = preproc_input(cubes.astype(np.float32))
    print(cubes.shape)
    preds = model.predict(cubes)
    preds = np.array(preds).mean()
    pred = np.squeeze(preds)
    return pred


def get_prediction(cube, model, preproc_input):
    pred = get_cube_pred_v2(model, cube, preproc_input)
    print('Float pred: {:.6f}'.format(pred))
    pred_binary = 0
    if pred > THR_FOR_MCC:
        pred_binary = 1
    return pred_binary


if __name__ == '__main__':
    cube = get_roi(TEST_VIDEO)
    print(cube.shape)
    model = load_zfturbo_model()
    _, preproc_input = Classifiers.get('densenet121')
    start_time = time.time()
    pred = get_prediction(cube, model, preproc_input)
    print('Prediction: {} Time: {:.2f} sec'.format(pred, time.time() - start_time))
    start_time = time.time()
    pred = get_prediction(cube, model, preproc_input)
    print('Prediction: {} Time: {:.2f} sec'.format(pred, time.time() - start_time))
    start_time = time.time()
    pred = get_prediction(cube, model, preproc_input)
    print('Prediction: {} Time: {:.2f} sec'.format(pred, time.time() - start_time))
