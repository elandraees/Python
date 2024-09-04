from util.database_util import insert_or_update_db_record, get_query_result
from util.date_util import now
from datetime import datetime

insert_column_order = "(api_method, account_id, request_url, request_body, request_date, response_code)"


def log_request(api_method, account_id, request, response):
    request_body = ""
    try:
        request_body = str(request.json)
    except Exception as e:
        request_body = ""

    insert_value_order = (api_method, account_id, request.url, request_body, now(), response.status_code)

    sql = "INSERT INTO api_log " + insert_column_order + "VALUES (%s, %s, %s, %s, %s, %s)"
    insert_or_update_db_record(sql, insert_value_order, None, None)
