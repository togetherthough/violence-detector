import os
from numpy import dtype
import numpy as np
import cv2
import yaml
import keras
from settings.config_loader import config


def load_video(path, max_frames= config.frames.MAX_FRAMES, resize = (config.frames.HEIGHT, config.frames.WIDTH)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret or frame_count >= max_frames:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, resize)
            frames.append(frame.astype(dtype))
            frame_count += 1

    finally:
        cap.release()
        
    while len(frames) < max_frames:
        frames.append(frames[-1].astype(dtype))

    return np.array(frames)


def prepare_dataset(folder_path):
    class_names = ["NonViolence", "Violence"]
    x, y = [], []
    for class_index, class_name in enumerate(class_names):
        class_folder = os.path.join(folder_path, class_name)
        video_cnt = 0
        for video_file in os.listdir(class_folder):
            if video_cnt > config.training.DATA_NUM:
                break
            video_path = os.path.join(class_folder, video_file)
            frames = load_video(video_path)
            x.append(frames)
            y.append(class_index)
            video_cnt += 1

    return np.array(x), keras.utils.to_categorical(y, num_classes=len(class_names))