from util.database_util import insert_or_update_db_record, get_query_results, get_query_result
import util.encryption_util as encryption_util
from models.account import Account
import util.constants as constants

account_insert_column_order = "(account_name, username, password, contact_number, " \
                              "email_address, status_id, create_date, last_update)"

account_load_column_order = "account_id, account_name, username, password, contact_number, " \
                            "email_address, status_id, create_date, last_update"


def create_account(account_data, cursor=None, db_connector=None):
    account_insert_value_order = (account_data.account_name, account_data.username,
                                  encryption_util.get_hashed_salt_value(account_data.password),
                                  account_data.contact_number, account_data.email_address,
                                  account_data.status_id, account_data.create_date, account_data.last_update)

    sql = "INSERT INTO accounts " + account_insert_column_order + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    insert_or_update_db_record(sql, account_insert_value_order, cursor, db_connector)


def get_account_list() -> [Account]:
    sql = "SELECT " + account_load_column_order + " from accounts "
    results = get_query_results(sql, (), None, None)
    if results is None or len(results) == 0:
        return []

    accounts = []
    for result in results:
        account_data = _get_account(result)
        accounts.append(account_data)

    return accounts


def get_account_by_username(username, cursor=None, db_connector=None) -> Account | None:
    sql = "SELECT " + account_load_column_order + " from accounts WHERE username = %s"
    result = get_query_result(sql, (username,), cursor, db_connector)
    return _get_account(result)


def get_account_by_id(account_id, cursor=None, db_connector=None) -> Account | None:
    sql = "SELECT " + account_load_column_order + " from accounts WHERE account_id = %s"
    result = get_query_result(sql, (account_id,), cursor, db_connector)
    return _get_account(result)


def get_account_by_email(email_address, cursor=None, db_connector=None) -> Account | None:
    sql = "SELECT " + account_load_column_order + " from accounts WHERE email_address = %s"
    result = get_query_result(sql, (email_address,), cursor, db_connector)
    return _get_account(result)


def delete_account(username, cursor=None, db_connector=None):
    sql = "DELETE from accounts where username = %s"
    insert_or_update_db_record(sql, (username,), cursor, db_connector)


def disable_account(username, cursor=None, db_connector=None):
    sql = "UPDATE accounts set status_id = %s where username = %s"
    insert_or_update_db_record(sql, (constants.MODEL_STATUS_TERMINATED, username), cursor, db_connector)


def update_account(account_data: Account, cursor=None, db_connector=None):
    sql = "UPDATE accounts set account_name = %s, email_address = %s, contact_number = %s," \
          " password= %s, status_id = %s, last_update = %s where username = %s"
    val = (account_data.account_name, account_data.email_address, account_data.contact_number,
           encryption_util.get_hashed_salt_value(account_data.password),
           account_data.status_id, account_data.last_update, account_data.username)
    insert_or_update_db_record(sql, val, cursor, db_connector)


def _get_account(sql_result) -> Account | None:
    if sql_result is None:
        return None

    db_id = sql_result[0]
    account_name = sql_result[1]
    username = sql_result[2]
    password = sql_result[3]
    contact_number = sql_result[4]
    email_address = sql_result[5]
    status_id = sql_result[6]
    create_date = sql_result[7]
    last_update = sql_result[8]

    return Account(account_name, username, password, email_address, contact_number, status_id,
                   create_date, last_update, db_id)
