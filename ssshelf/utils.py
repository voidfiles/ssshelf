import datetime
import time
import json
from uuid import UUID
import re
from urllib.parse import quote_plus


def camelcase_to_dash(s):
    # stolen from http://stackoverflow.com/a/1176023
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


class RaiseNotImplemented(object):
    def __get__(self, instance, owner):
        raise NotImplementedError

RAISE_NOT_IMPLEMENTED = RaiseNotImplemented()


def convert_datetime_to_str(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def type_handler(x):
    if isinstance(x, datetime.datetime):
        return x.strftime("%Y-%m-%dT%H:%M:%SZ")

    if isinstance(x, UUID):
        return str(x)

    raise TypeError("Unknown type")


def json_dump(*args, **kwargs):
    kwargs.setdefault('default', type_handler)

    return json.dumps(*args, **kwargs)


def build_url_path(parts):
    return '/'.join([quote_plus(x) for x in parts])


def datetime_to_secs(dt):
    return int(time.mktime(dt.timetuple()))
