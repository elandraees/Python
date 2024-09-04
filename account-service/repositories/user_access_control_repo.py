from util.database_util import insert_or_update_db_record, get_query_result, get_query_results, insert_many_into_db
from models.user_access_control import UserAccessControl

access_user_control_columns = 'control_id, user_id, account_id, status_id, create_date, last_update, id'

access_user_control_insert_columns = '(control_id, user_id, account_id, status_id, create_date, last_update)'


def get_control_for_user(user_id, control_id, cursor=None, db_connector=None) -> UserAccessControl | None:
    sql = 'SELECT ' + access_user_control_columns + ' from user_access_controls where user_id = %s and control_id = %s'
    result = get_query_result(sql, (user_id, control_id), cursor, db_connector)
    return __get_user_access_control(result)


def get_all_control_for_user(user_id, cursor=None, db_connector=None) -> [UserAccessControl]:
    sql = 'SELECT ' + access_user_control_columns + ' from user_access_controls where user_id = %s'
    results = get_query_results(sql, (user_id,), cursor, db_connector)
    if results is None or len(results) == 0:
        return []

    return [__get_user_access_control(result) for result in results]


def create_user_access_controls(user_controls: [UserAccessControl], cursor=None, db_connector=None):
    sql = 'INSERT INTO user_access_controls ' + access_user_control_insert_columns + ' VALUES (%s, %s, %s, %s, %s, %s)'
    val = [(user_control.control_id, user_control.user_id, user_control.account_id, user_control.status_id,
           user_control.create_date, user_control.last_update) for user_control in user_controls]
    insert_many_into_db(sql, val, cursor, db_connector)


def delete_user_access_controls(user_controls: [UserAccessControl], cursor=None, db_connector=None):
    sql = 'DELETE from user_access_controls WHERE control_id = %s and user_id = %s'
    val = [(user_control.control_id, user_control.user_id) for user_control in user_controls]
    insert_many_into_db(sql, val, cursor, db_connector)


def __get_user_access_control(sql_result) -> UserAccessControl | None:
    if sql_result is None:
        return None

    control_id = sql_result[0]
    user_id = sql_result[1]
    account_id = sql_result[2]
    status_id = sql_result[3]
    create_date = sql_result[4]
    last_update = sql_result[5]
    db_id = sql_result[6]

    return UserAccessControl(control_id, user_id, account_id, status_id, create_date, last_update, db_id)
