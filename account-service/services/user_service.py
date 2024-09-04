import util.jwt_util as jwt_util
import repositories.user_repo as user_repo
import util.json_util as json_util
import util.constants as constants
from models.user import User
from models.account import Account
import services.account_service as account_service
import util.validation_util as validation_util


def get_user_auth_token(username) -> dict:
    user_data: User = get_user(username)
    account: Account = account_service.get_account_by_id(user_data.account_id)

    if not account.is_active():
        raise Exception('This account is not active on our system.')

    jwt_token = jwt_util.create_token(user_data.account_id, user_data.username, account.username)

    return {'token': jwt_token}


def get_user_list(account_id) -> [dict]:
    user_list: [User] = user_repo.get_users_by_account_id(account_id)
    user_list_response: [dict] = [user_data.to_json_include_id() for user_data in user_list]
    return user_list_response


def create_user(json, account_username) -> User:
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    account: Account = account_service.get_account(account_username)

    user: User = __get_user_from_json(account.account_id, constants.USER_TYPE_SECONDARY, json, False)
    errors = user.validate(False)
    if errors:
        raise Exception(errors)

    user_repo.create_user(user)

    return user


def update_user(json, username, account_id):
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    existing_user: User = get_user_by_account_id(username, account_id)
    user: User = __get_user_from_json(account_id, constants.USER_TYPE_SECONDARY, json, True)

    existing_user.update(user)

    errors = existing_user.validate(True)
    if errors:
        raise Exception(errors)

    user_repo.update_user(existing_user)


def delete_user(username, account_username):
    account: Account = account_service.get_account(account_username)
    user_repo.delete_user_by_username_and_account_id(username, account.account_id)


def create_main_user(json, account_id, cursor, db_connector) -> User:
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    user: User = __get_user_from_json(account_id, constants.USER_TYPE_MAIN, json, False)
    errors = user.validate(False)
    if errors:
        raise Exception(errors)

    user_repo.create_user(user, cursor, db_connector)

    return user


def update_main_user(json, username, account_id, cursor=None, db_connector=None):
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    user: User = __get_user_from_json(account_id, constants.USER_TYPE_MAIN, json, True)
    existing_user = get_user_by_account_id(username, account_id)
    existing_user.update(user)

    errors = existing_user.validate(True)
    if errors:
        raise Exception(errors)

    user_repo.update_user(existing_user, cursor, db_connector)


def delete_main_users(account_id, cursor, db_connector):
    user_repo.delete_user_by_account_id(account_id, cursor, db_connector)


def disable_user(username, account_username):
    account: Account = account_service.get_account(account_username)
    user_repo.disable_user(username, account.account_id)


def disable_all_users(account_id):
    user_repo.disable_all_users(account_id)


def get_user(username) -> User:
    user_data: User = user_repo.get_user_by_username(username)

    if user_data is None:
        raise Exception(f'"Cannot find account for username: {username}')

    return user_data


def get_user_by_account_id(username, account_id) -> User:
    user_data: User = user_repo.get_user_by_username_and_account_id(username, account_id)

    if user_data is None:
        raise Exception(f'"Cannot find account for username: {username}')

    return user_data


def __get_user_from_json(account_id, user_type_id, data, is_update) -> User:
    try:
        username = json_util.parse_json(data, 'username')
        contact_number = json_util.parse_json(data, 'contact_number')
        email_address = json_util.parse_json(data, 'email_address')
        password = json_util.parse_json(data, 'password')
        first_name = json_util.parse_json(data, 'first_name')
        last_name = json_util.parse_json(data, 'last_name')
        status = json_util.parse_json(data, 'status')
        status_id = __resolve_user_status_id(status, is_update, user_type_id == constants.USER_TYPE_MAIN)

        if validation_util.is_none_empty_or_zero(username):
            username = email_address

        return User(account_id, first_name, last_name, username, password, email_address,
                    contact_number, status_id, user_type_id)

    except Exception as e:
        raise Exception(str(e))


def __resolve_user_status_id(status, is_update, is_main_user) -> int:
    # if no status found and is not an update
    if validation_util.is_none_empty_or_zero(status) and not is_update:
        return constants.MODEL_STATUS_ACTIVE

    if validation_util.is_none_empty_or_zero(status) or is_main_user:
        return 0

    # if there is a status try and resolve the status id
    if status in constants.MODEL_STATUS_MAP:
        return constants.MODEL_STATUS_MAP[status]

    return -1
