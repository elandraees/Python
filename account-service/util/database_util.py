from psycopg2 import connect


def get_db_connection():
    mydb = connect(
        host="localhost",
        user="postgres",
        password="zxcvbnm",
        database="account-service"
    )
    return mydb


'''
return a list of tuples
[(),(),()]
'''


def get_query_results(sql, val, cursor=None, db_connector=None):
    commit = False
    if db_connector is None:
        db_connector = get_db_connection()
        commit = True

    try:
        if cursor is None:
            cursor = db_connector.cursor()
        cursor.execute(sql, val)

        return cursor.fetchall()

    except Exception as e:
        if commit:
            db_connector.rollback()
        raise Exception('Unable to execute query: ' + str(e))
    finally:
        if commit:
            db_connector.commit()


'''
returns single tuple ()
'''


def get_query_result(sql, val, cursor=None, db_connector=None):
    commit = False
    if db_connector is None:
        db_connector = get_db_connection()
        commit = True

    try:
        if cursor is None:
            cursor = db_connector.cursor()
        cursor.execute(sql, val)

        return cursor.fetchone()

    except Exception as e:
        if commit:
            db_connector.rollback()
        raise Exception('Unable to execute query: ' + str(e))
    finally:
        if commit:
            db_connector.commit()


def insert_or_update_db_record(sql, val, cursor=None, db_connector=None):
    commit = False
    if db_connector is None:
        db_connector = get_db_connection()
        commit = True

    try:
        if cursor is None:
            cursor = db_connector.cursor()
        cursor.execute(sql, val)
    except Exception as e:
        if commit:
            db_connector.rollback()
        raise Exception('Unable to execute query: ' + str(e))
    finally:
        if commit:
            db_connector.commit()


def insert_many_into_db(sql, val, cursor=None, db_connector=None):
    commit = False
    if db_connector is None:
        db_connector = get_db_connection()
        commit = True

    try:
        if cursor is None:
            cursor = db_connector.cursor()
        cursor.executemany(sql, val)
    except Exception as e:
        if commit:
            db_connector.rollback()
        raise Exception('Unable to execute query: ' + str(e))
    finally:
        if commit:
            db_connector.commit()
