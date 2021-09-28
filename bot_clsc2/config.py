import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CREDS_DIR = os.path.join(BASE_DIR, "credentials")
