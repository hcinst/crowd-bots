import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")
BEST_MODEL_PATH = os.path.join(MODELS_DIR, "merged_model_5_False.h5")
CREDS_DIR = os.path.join(BASE_DIR, "credentials")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
TEST_VIDEO = os.path.join(BASE_DIR, "videos", "100152.mp4")
sys.path.append(os.path.abspath(os.path.dirname(BASE_DIR)))
# print(os.path.abspath(os.path.dirname(BASE_DIR)))