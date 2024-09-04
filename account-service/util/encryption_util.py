import bcrypt
import secrets
import string
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


def get_encrypted_value(value):
    return value
    # key = constants.ENCRYPT_KEY
    # fernet = Fernet(key)
    # encrypted_value = fernet.encrypt(value.encode('utf-8'))
    # return encrypted_value.decode('utf8')


def get_decrypted_value(value):
    return value
    # key = constants.ENCRYPT_KEY
    # fernet = Fernet(key)
    # return fernet.decrypt(value).decode('utf8')


def get_hashed_salt_value(value):
    pwd_bytes = value.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    string_password = hashed_password.decode('utf8')
    return string_password


def check_hash(to_check, value):
    password_byte_enc = to_check.encode('utf-8')
    hashed_password = value.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password)


def generate_random_password():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                   for i in range(10))


def generate_random_token():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                   for i in range(15))
