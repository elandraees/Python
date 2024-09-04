import util.encryption_util as encryption_util
import util.jwt_util as jwt_util
import util.constants as constants
import repositories.account_repo as account_repo
from base64 import b64decode, b64encode
import util.validation_util as validation_util
from functools import wraps
import util.api_response as api_response
from flask import Blueprint, request
import datetime
import services.account_service as account_service
import services.user_service as user_service
import util.json_util as json_util
from models.account import Account
from models.user import User
from models.user_access_control import UserAccessControl
import repositories.api_log_repo as api_log_repo
import services.user_access_service as user_access_service
from datetime import datetime, timedelta

account_api_key = ""
username = ""
account_username = ""
password = ""
account_id = 0


def authenticate_secret(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        service_key = request.headers.get(constants.SECRET_KEY_HEADER)
        if validation_util.is_none_empty_or_zero(service_key) or service_key != constants.SECRET_KEY:
            return api_response.get_error_response("Insufficient Authorization", "", 401)

        return fn(*args, **kwargs)

    return wrapper


def authenticate_user_password(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global username
        global password
        global account_id
        header = request.headers.get(constants.AUTH_HEADER)
        if header is None or not header.startswith(constants.BASIC_AUTH_HEADER):
            return api_response.get_error_response("Insufficient Authorization", "", 401)
        token = header[6:]
        username, password = b64decode(token).decode().split(':', 1)
        if not username or not password:
            return api_response.get_error_response("No Username or Password Specified", "", 401)

        user: User = user_service.get_user(username)
        account: Account = account_service.get_account_by_id(user.account_id)
        if not encryption_util.check_hash(password, account.password):
            return api_response.get_error_response("Password or Username is incorrect", "", 401)
        account_id = account.account_id

        return fn(*args, **kwargs)

    return wrapper


def authenticate_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        __decode_token()
        return fn(*args, **kwargs)

    return wrapper


def authenticate_token_and_main_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        __decode_token()
        if get_username() != get_account_username():
            return api_response.get_error_response("Insufficient Authorization", "", 401)
        return fn(*args, **kwargs)

    return wrapper


def authenticate_token_access(*control_ids):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            __decode_token()

            access_controls: [UserAccessControl] = user_access_service.get_all_controls_for_user(get_username())

            if control_ids not in [access_control.control_id for access_control in access_controls]:
                return api_response.get_error_response("Insufficient Authorization", "", 401)

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def authenticate_token_access_or_main_user(*control_ids):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            __decode_token()

            if get_username() == get_account_username():
                return fn(*args, **kwargs)

            access_controls: [UserAccessControl] = user_access_service.get_all_controls_for_user(get_username())
            access_controls_ids = [access_control.control_id for access_control in access_controls]

            if not any(control in access_controls_ids for control in control_ids):
                return api_response.get_error_response("Insufficient Authorization", "", 401)

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def authenticate_token_access_or_self(*control_ids):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            __decode_token()

            user = request.args.get('username')
            if validation_util.is_none_empty_or_zero(user):
                return api_response.get_error_response("An error has occurred", "Please specify the username", 400)

            the_user: User = user_service.get_user(user)

            if the_user.account_id != account_id:
                return api_response.get_error_response("Insufficient Authorization", "", 401)

            if user == get_username() or get_username() == get_account_username():
                return fn(*args, **kwargs)

            access_controls: [UserAccessControl] = user_access_service.get_all_controls_for_user(get_username())
            access_controls_ids = [access_control.control_id for access_control in access_controls]

            if not any(control in access_controls_ids for control in control_ids):
                return api_response.get_error_response("Insufficient Authorization", "", 401)

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def __decode_token() -> str | None:
    global username
    global account_username
    global account_id
    jwt_decoded_token = jwt_util.get_decoded_token(request)
    if jwt_decoded_token is None:
        return api_response.get_error_response("Insufficient Authorization", "", 401)
    exp = jwt_decoded_token.get(constants.JWT_PAYLOAD_EXP)
    if exp < int(datetime.utcnow().timestamp()):
        return api_response.get_error_response("Insufficient Authorization", "", 401)
    account_id = jwt_decoded_token.get(constants.JWT_PAYLOAD_ACCOUNT_ID)
    username = jwt_decoded_token.get(constants.JWT_PAYLOAD_USERNAME)
    account_username = jwt_decoded_token.get(constants.JWT_PAYLOAD_ACCOUNT_USERNAME)
    if username is None or account_id is None or account_username is None:
        return api_response.get_error_response("Insufficient Authorization", "", 401)


def get_username():
    return username


def get_account_username():
    return account_username


def get_account_id():
    return account_id
