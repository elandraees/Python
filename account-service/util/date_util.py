from datetime import datetime, timedelta

db_date_format = '%Y-%m-%d %H:%M:%S'
basic_date_format = '%d-%m-%Y'


def get_datetime(date, old_format, new_format):
    return datetime.strptime(date, old_format).strftime(new_format)


def now():
    return datetime.now().strftime(db_date_format)


def get_start_of_next_month():
    dt = datetime.now()
    return (dt.replace(day=1) + timedelta(days=32)).replace(day=1).replace(microsecond=0)
