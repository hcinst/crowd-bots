import os
from datetime import datetime
from datetime import timedelta

from bot_clsc2.config import LOGS_DIR, DATA_DIR, CREDS_DIR
from bot_clsc2.model import CLSC2


def read_credentials(file_path):
    with open(file_path) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        return lines


if __name__ == "__main__":
    api_version = "dev"

    credentials_file = os.path.join(CREDS_DIR, "clsc2.txt")
    email_address, username, password = read_credentials(credentials_file)

    duration = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=1, hours=0, weeks=0)

    model = CLSC2(api_version, username, password, email_address, LOGS_DIR, DATA_DIR, None, duration)
    model.run()
