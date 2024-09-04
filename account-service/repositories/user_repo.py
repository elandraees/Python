from util.database_util import insert_or_update_db_record, get_query_result, get_query_results
import util.encryption_util as encryption_util
from models.user import User
import util.constants as constants

user_insert_column_order = "(account_id, username, password, first_name, last_name, contact_number, email_address," \
                           "user_type_id, status_id, create_date, last_update)"

user_load_column_order = "user_id, account_id, username, password, first_name, last_name, contact_number, " \
                         "email_address, user_type_id, status_id, create_date, last_update"


def create_user(user_data, cursor=None, db_connector=None):
    user_insert_value_order = (user_data.account_id, user_data.username,
                               encryption_util.get_hashed_salt_value(user_data.password)
                               , user_data.first_name, user_data.last_name, user_data.contact_number,
                               user_data.email_address, user_data.user_type_id,
                               user_data.status_id, user_data.create_date, user_data.last_update)

    sql = "INSERT INTO users " + user_insert_column_order + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_or_update_db_record(sql, user_insert_value_order, cursor, db_connector)


def update_user(user: User, cursor=None, db_connector=None):
    sql = "UPDATE users set first_name = %s, last_name = %s, email_address = %s, contact_number = %s," \
          " password= %s, status_id = %s, last_update = %s where username = %s"
    val = (user.first_name, user.last_name, user.email_address, user.contact_number,
           encryption_util.get_hashed_salt_value(user.password),
           user.status_id, user.last_update, user.username)
    insert_or_update_db_record(sql, val, cursor, db_connector)


def get_user_by_username(username, cursor=None, db_connector=None) -> User | None:
    sql = "SELECT " + user_load_column_order + " from users WHERE username = %s"
    result = get_query_result(sql, (username,), cursor, db_connector)
    return _get_user(result)


def get_user_by_username_and_account_id(username, account_id, cursor=None, db_connector=None) -> User | None:
    sql = "SELECT " + user_load_column_order + " from users WHERE username = %s and account_id = %s"
    result = get_query_result(sql, (username, account_id), cursor, db_connector)
    return _get_user(result)


def get_users_by_account_id(account_id, cursor=None, db_connector=None) -> [User]:
    sql = "SELECT " + user_load_column_order + " from users WHERE account_id = %s"
    results = get_query_results(sql, (account_id,), cursor, db_connector)
    if results is None or len(results) == 0:
        return []

    users = []
    for result in results:
        user_data = _get_user(result)
        users.append(user_data)

    return users


def delete_user_by_account_id(account_id, cursor=None, db_connector=None):
    sql = "DELETE from users where account_id = %s"
    insert_or_update_db_record(sql, (account_id,), cursor, db_connector)


def delete_user_by_username_and_account_id(username, account_id, cursor=None, db_connector=None):
    sql = "DELETE from users where username = %s and account_id = %s"
    insert_or_update_db_record(sql, (username, account_id), cursor, db_connector)


def disable_all_users(account_id, cursor=None, db_connector=None):
    sql = "UPDATE users set status_id = % where account_id = %s"
    insert_or_update_db_record(sql, (constants.MODEL_STATUS_TERMINATED, account_id), cursor, db_connector)


def disable_user(username, account_id, cursor=None, db_connector=None):
    sql = "UPDATE users set status_id = % where username = %s and account_id = %s"
    insert_or_update_db_record(sql, (constants.MODEL_STATUS_TERMINATED, username, account_id), cursor, db_connector)


def _get_user(sql_result) -> User | None:
    if sql_result is None:
        return None

    db_id = sql_result[0]
    account_id = sql_result[1]
    username = sql_result[2]
    password = sql_result[3]
    first_name = sql_result[4]
    last_name = sql_result[5]
    contact_number = sql_result[6]
    email_address = sql_result[7]
    user_type_id = sql_result[8]
    status_id = sql_result[9]
    create_date = sql_result[10]
    last_update = sql_result[11]

    return User(account_id, first_name, last_name, username, password, email_address, contact_number,
                status_id, user_type_id, create_date, last_update, db_id)
