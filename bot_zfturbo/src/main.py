if __name__ == '__main__':
    import os

    gpu_use = 4
    print('GPU use: {}'.format(gpu_use))
    os.environ["KERAS_BACKEND"] = "tensorflow"
    os.environ["CUDA_VISIBLE_DEVICES"] = "{}".format(gpu_use)
    
import os
import sys
from datetime import datetime
from datetime import timedelta


inc_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(inc_dir)
sys.path.append(os.path.abspath(os.path.dirname(inc_dir)))

from bot_zfturbo.src.bot_file import ZFTurbo
from bot_zfturbo.config import BASE_DIR, CREDS_DIR, LOGS_DIR, DATA_DIR


def read_credentials(file_path):
    with open(file_path) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


if __name__ == "__main__":
    api_version = "prod"
    if api_version == 'prod':
        credentials_file = os.path.join(CREDS_DIR, "zfturbo.txt")
    else:
        credentials_file = os.path.join(CREDS_DIR, "zfturbo-dev.txt")
    email_address, username, password = read_credentials(credentials_file)
    # print(BASE_DIR, email_address, username, password)
    if api_version == 'prod':
        # start_time = datetime(year=2021, month=10, day=6, hour=19, minute=0, second=0, microsecond=0)
        start_time = None
        duration = None
    else:
        start_time = None
        duration = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=5, hours=0, weeks=0)
    zf_bot = ZFTurbo(api_version, username, password, email_address, LOGS_DIR, DATA_DIR, start_time, duration)
    zf_bot.run()
