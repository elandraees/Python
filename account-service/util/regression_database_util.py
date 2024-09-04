from psycopg2 import connect
import util.database_util as database_util


def get_db_connection():
    mydb = connect(
        host="localhost",
        user="postgres",
        password="zxcvbnm",
        database="account-service-regression"
    )
    return mydb


def get_query_results(sql, val, cursor=None):
    return database_util.get_query_results(sql, val, cursor, get_db_connection())


def get_query_result(sql, val, cursor=None):
    return database_util.get_query_result(sql, val, cursor, get_db_connection())


def insert_or_update_db_record(sql, val, cursor=None, db_connector=None):
    database_util.insert_or_update_db_record(sql, val, cursor, get_db_connection())


def insert_many_into_db(sql, val, cursor=None, db_connector=None):
    database_util.insert_many_into_db(sql, val, cursor, get_db_connection())
