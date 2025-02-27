import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

MODEL_STATUS_PENDING = 0
MODEL_STATUS_ACTIVE = 1
MODEL_STATUS_SUSPENDED = 2
MODEL_STATUS_TERMINATED = 3

MODEL_STATUS_MAP_ID = {
    0: "PENDING",
    1: "ACTIVE",
    2: "SUSPENDED",
    3: "TERMINATED"
}

MODEL_STATUS_MAP = {
    "PENDING": 0,
    "ACTIVE": 1,
    "SUSPENDED": 2,
    "TERMINATED": 3
}

USER_TYPE_MAIN = 1
USER_TYPE_SECONDARY = 2

ACCOUNT_ACCESS_CONTROL_ID = 10000
VIEW_ALL_USERS_ACCESS_CONTROL_ID = 10001
EDIT_ALL_USERS_ACCESS_CONTROL_ID = 10002
DELETE_ALL_USERS_ACCESS_CONTROL_ID = 10003

API_KEY_HEADER = 'API-Key'
AUTH_HEADER = 'Authorization'
BASIC_AUTH_HEADER = 'Basic '
BEARER_AUTH_HEADER = 'Bearer '
USERNAME_HEADER = 'Username'
SECRET_KEY_HEADER = 'Secret-Key'

JWT_ALGORITHM = 'HS256'
JWT_PAYLOAD_USERNAME = 'username'
JWT_PAYLOAD_ACCOUNT_ID = 'account_id'
JWT_PAYLOAD_ACCOUNT_USERNAME = 'account_username'
JWT_PAYLOAD_EXP = 'exp'

SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_JWT_KEY = os.getenv('SECRET_JWT_KEY')



