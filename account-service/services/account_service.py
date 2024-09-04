import util.json_util as json_util
import repositories.account_repo as account_repo
import util.constants as constants
from models.account import Account
import util.validation_util as validation_util
import services.user_service as user_service
from util.database_util import get_db_connection


def create_account(json) -> Account:
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    account_data = get_account_from_json(json, False)
    errors = account_data.validate(False)

    if errors:
        raise Exception(errors)

    # create account and user in same transaction
    db_connector = get_db_connection()
    try:
        cursor = db_connector.cursor()
        account_repo.create_account(account_data, cursor, db_connector)
        account_data: Account = account_repo.get_account_by_username(account_data.username, cursor, db_connector)
        account_id = account_data.account_id
        user_service.create_main_user(json, account_id, cursor, db_connector)
    except Exception as e:
        db_connector.rollback()
        raise Exception(e)
    finally:
        db_connector.commit()

    return account_data


def delete_account(username):
    if validation_util.is_none_empty_or_zero(username):
        raise Exception('No username found')

    account_data = account_repo.get_account_by_username(username)

    if account_data is None:
        raise Exception(f"Cannot find account for username: {username}")

    # delete account and users in one transaction
    db_connector = get_db_connection()
    try:
        cursor = db_connector.cursor()
        account_repo.delete_account(username, cursor, db_connector)
        account_id = account_data.account_id
        user_service.delete_main_users(account_id, cursor, db_connector)
    except Exception as e:
        db_connector.rollback()
        raise Exception('Unable to delete account ' + str(e))
    finally:
        db_connector.commit()

    return account_data


def disable_account(username):
    account_data: Account = get_account(username)
    account_repo.disable_account(username)
    user_service.disable_all_users(account_data.account_id)


def update_account(json, username):
    if not validation_util.is_none_empty_or_zero(json_util.parse_json(json, 'createAccountHidden')):
        raise Exception('Invalid')

    account_data: Account = get_account_from_json(json, True)
    existing_account: Account = get_account(username)
    existing_account.update(account_data)
    errors = existing_account.validate(True)

    if errors:
        raise Exception(errors)

    # update account and user in one transaction
    db_connector = get_db_connection()
    try:
        cursor = db_connector.cursor()
        account_repo.update_account(existing_account, cursor, db_connector)
        account_id = existing_account.account_id
        user_service.update_main_user(json, username, account_id, cursor, db_connector)
    except Exception as e:
        db_connector.rollback()
        raise Exception('Unable to update account ' + str(e))
    finally:
        db_connector.commit()

    return existing_account


def get_account_list() -> [dict]:
    account_list: [Account] = account_repo.get_account_list()
    account_list_response: [dict] = [account_data.to_json_include_id() for account_data in account_list]
    return account_list_response


def get_account(username) -> Account:
    account_data: Account = account_repo.get_account_by_username(username)

    if account_data is None:
        raise Exception(f'"Cannot find account for username: {username}')

    return account_data


def get_account_by_id(account_id) -> Account:
    account_data: Account = account_repo.get_account_by_id(account_id)

    if account_data is None:
        raise Exception(f'"Cannot find account')

    return account_data


def get_account_from_json(data, is_update) -> Account:

    if not validation_util.is_none_empty_or_zero(json_util.parse_json(data, 'createAccountHidden')):
        raise Exception('Invalid')

    try:
        username = json_util.parse_json(data, 'username')
        contact_number = json_util.parse_json(data, 'contact_number')
        email_address = json_util.parse_json(data, 'email_address')
        password = json_util.parse_json(data, 'password')
        account_name = json_util.parse_json(data, 'account_name')
        status = json_util.parse_json(data, 'status')
        status_id = __resolve_account_status_id(status, is_update)

        if validation_util.is_none_empty_or_zero(username):
            username = email_address
        if validation_util.is_none_empty_or_zero(account_name):
            account_name = email_address

        return Account(account_name, username, password, email_address,
                       contact_number, status_id)

    except Exception as e:
        raise Exception(str(e))


def __resolve_account_status_id(status, is_update) -> int:
    # if no status found and is not an update
    if validation_util.is_none_empty_or_zero(status) and not is_update:
        return constants.MODEL_STATUS_ACTIVE

    # if validation_util.is_none_empty_or_zero(status):
    #     return 0
    #
    # # if there is a status try and resolve the status id
    # if status in constants.MODEL_STATUS_MAP:
    #     return constants.MODEL_STATUS_MAP[status]

    return 0
