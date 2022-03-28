from pathlib import Path
import json


FILES_FOLDER = "attached"
LOG_FOLDER = "log"
FILE_LIFE_TIME = 14

SERVER_HOST = "localhost"
SERVER_PORT = 9000

PATH = Path(__file__).resolve().parent

with open("config.json", 'r', encoding='UTF-8') as f:
    json_data = f.read()
    connect_data = json.loads(json_data)
    EMAIL_HOST = connect_data["EMAIL_HOST"]
    EMAIL_PORT = connect_data["EMAIL_PORT"]
    EMAIL_HOST_PASSWORD = connect_data["EMAIL_HOST_PASSWORD"]
    EMAIL_HOST_USER = connect_data["EMAIL_HOST_USER"]
