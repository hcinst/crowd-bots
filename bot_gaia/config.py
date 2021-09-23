import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")
R2PLUS1D_DIR = os.path.join(MODELS_DIR, "R(2+1)D")
MC3_DIR = os.path.join(MODELS_DIR, "MC3")
R3D_DIR = os.path.join(MODELS_DIR, "R3D")
BEST_R2PLUS1_MODEL_PATH = os.path.join(R2PLUS1D_DIR, "model_v65_epoch_28_mcc_0.769_acc_0.9635_loss0.1323.pth")
BEST_MC3_MODEL_PATH = os.path.join(MC3_DIR, "model_v66_epoch_28_mcc_0.7989_acc_0.9673_loss0.1125.pth")
BEST_R3D_MODEL_PATH = os.path.join(R3D_DIR, "model_v67_epoch_27_mcc_0.7801_acc_0.9635_loss0.1248.pth")
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CREDS_DIR = os.path.join(BASE_DIR, "credentials")
