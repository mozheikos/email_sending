from typing import Tuple, Union, Any
from crontab import CronTab
from settings import PATH, EMAIL_HOST_USER, FILES_FOLDER, LOG_FOLDER
from email.message import EmailMessage
from bottle import Request
import os
import datetime
import logging


def get_logger() -> logging.Logger:
    if LOG_FOLDER not in os.listdir(PATH):
        os.mkdir(f"{PATH}/{LOG_FOLDER}")

    date = datetime.date.today()

    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f"{PATH}/{LOG_FOLDER}/{date}.log")
    log_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    file_handler.setFormatter(log_format)

    logger.addHandler(file_handler)

    return logger


def set_crontab_task() -> dict:
    cron = CronTab(user="stanislav")

    command = f"python3 {PATH}/archive_deleter.py"

    exists = False
    for item in cron.find_command("archive_deleter"):
        if item:
            exists = True
            break

    if not exists:

        try:
            job = cron.new(command=command, comment="archive_deleter")
            job.hour.every(24)
            cron.write()
        except Exception as e:
            message = str(e)
            status = False
        else:
            message = "task successfully added"
            status = True

    else:
        status = True
        message = "task already exists"

    return {"status": status, "message": message}


def get_letter(request: Request) -> tuple:
    from_addr = EMAIL_HOST_USER

    addresses = request.forms["to"]
    to_addr = addresses.split(",")
    subject = request.forms.get("subject")

    msg = request.forms.get("message")

    letter = EmailMessage()
    letter["From"] = from_addr
    letter["Subject"] = subject
    letter.set_content(msg)

    return from_addr, to_addr, letter


def attach_file(request: Request, letter: EmailMessage) -> Tuple[EmailMessage, Union[str, Any]]:

    file = request.files.get("file")
    folder = FILES_FOLDER
    path = PATH

    if folder not in os.listdir(path):
        os.mkdir(os.path.join(path, folder))

    prefix = "_".join(str(datetime.datetime.now()).split(" "))

    file.filename = prefix + "_" + file.filename
    save_path = os.path.join(path, folder)
    file.save(save_path)

    subtype = file.filename.rsplit(".", 1)[-1]

    with open(f"{save_path}/{file.filename}", "rb") as f:
        attached_file = f.read()

    letter.add_attachment(attached_file, maintype="bytes", subtype=subtype, filename=file.filename)

    return letter, file.filename
