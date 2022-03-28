import datetime
import os
from settings import FILES_FOLDER, PATH, LOG_FOLDER, FILE_LIFE_TIME
import logging
from handlers import get_logger


def delete_file(path: str, filename: str, logger: logging.Logger) -> None:
    os.remove(os.path.join(path, filename))
    logger.info(f"file {FILES_FOLDER}/{filename} deleted (reason: time elapsed)")


def get_file_age(filename: str) -> datetime:
    data = filename.split("-")
    file_data = datetime.date(*[int(x) for x in data])
    return file_data


def run():
    logger = get_logger()
    now_date = datetime.date.today()

    attachments_path = os.path.join(PATH, FILES_FOLDER)
    log_path = os.path.join(PATH, LOG_FOLDER)

    for filename in os.listdir(attachments_path):
        filename = str(filename)
        str_file_data = filename.split("_", 1)[0]

        file_data = get_file_age(filename=str_file_data)

        exp_time = now_date - datetime.timedelta(days=FILE_LIFE_TIME)
        if file_data < exp_time:
            delete_file(path=attachments_path, filename=filename, logger=logger)

    for filename in os.listdir(log_path):
        filename = str(filename)
        str_file_data = filename[:-4]
        file_data = get_file_age(filename=str_file_data)

        exp_time = now_date - datetime.timedelta(days=FILE_LIFE_TIME)
        if file_data < exp_time:
            delete_file(path=log_path, filename=filename, logger=logger)


if __name__ == "__main__":
    run()
