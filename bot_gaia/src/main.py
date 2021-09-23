import os
from datetime import datetime
from datetime import timedelta

from bot_gaia.src.gaia import Gaia
from bot_gaia.config import LOGS_DIR, DATA_DIR, CREDS_DIR


def read_credentials(file_path):
    with open(file_path) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


if __name__ == "__main__":
    api_version = "dev"
    credentials_file = os.path.join(CREDS_DIR, "gaia.txt")
    email_address, username, password = read_credentials(credentials_file)
    # start_time = datetime(year=2021, month=9, day=21, hour=12, minute=16, second=0, microsecond=0)
    duration = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=1, hours=0, weeks=0)
    gaia = Gaia(api_version, username, password, email_address, LOGS_DIR, DATA_DIR, None, duration)
    gaia.run()
