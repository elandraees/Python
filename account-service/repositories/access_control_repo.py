from util.database_util import insert_or_update_db_record, get_query_result, get_query_results
from models.access_control import AccessControl

access_control_columns = 'control_id, name, description, control_type_id, control_level_id, ' \
                         'status_id, create_date, last_update'

access_control_insert_columns = '(control_id, name, description, control_type_id, control_level_id, ' \
                                'status_id, create_date, last_update)'


def get_control(control_id, cursor=None, db_connector=None) -> AccessControl:
    sql = 'SELECT ' + access_control_columns + ' from access_controls where control_id = %s'
    result = get_query_result(sql, (control_id,), cursor, db_connector)
    return __get_access_control(result)


def create_access_control(access_control: AccessControl, cursor=None, db_connector=None):
    sql = 'INSERT INTO access_controls ' + access_control_insert_columns + \
          ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    val = (access_control.control_id, access_control.name, access_control.description, access_control.control_type_id,
           access_control.control_level_id, access_control.status_id,
           access_control.create_date, access_control.last_update)
    insert_or_update_db_record(sql, val, cursor, db_connector)


def __get_access_control(sql_result) -> AccessControl | None:
    if sql_result is None:
        return None

    control_id = sql_result[0]
    name = sql_result[1]
    description = sql_result[2]
    control_type_id = sql_result[3]
    control_level_id = sql_result[4]
    status_id = sql_result[5]
    create_date = sql_result[6]
    last_update = sql_result[7]

    return AccessControl(control_id, name, description, control_type_id,
                                        control_level_id, status_id, create_date, last_update)
