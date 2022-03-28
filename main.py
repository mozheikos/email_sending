import smtplib
import os
import settings
from bottle import run, post, request
from handlers import ser_crontab_task, attach_file, get_logger, get_letter

logger = get_logger()


@post("/")
def send_email() -> None:

    logger.info(f"receiving request")

    from_addr, to_addr, letter = get_letter(request=request)

    file = request.files.get("file")
    filename = None
    if file:
        letter, filename = attach_file(request=request, letter=letter)

    count = 0
    while count <= 5:
        try:
            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(letter, from_addr=from_addr, to_addrs=to_addr)
            server.quit()
        except Exception as e:
            logger.error(e)
            continue
        else:
            logger.info("message sent successfully")
            count = 6
            if file:
                file_path = os.path.join(settings.PATH, settings.FILES_FOLDER, filename)
                os.remove(file_path)
                logger.info(f"file {file_path} removed")


if __name__ == "__main__":

    status = ser_crontab_task()

    if status["status"]:
        logger.info(status["message"])
    else:
        logger.error(status["message"])

    host = settings.SERVER_HOST
    port = settings.SERVER_PORT

    run(host=host, port=port)
