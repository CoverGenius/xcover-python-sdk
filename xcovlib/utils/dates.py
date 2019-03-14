from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time


def http_date():
    now = datetime.utcnow()
    return format_date_time(mktime(now.timetuple()))
