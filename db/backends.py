"""A module that regroups a list of functions and classes backends
for basics operations on the database e.g. opening, reading or writing
data to the database.
"""

import functools
import io
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from requests import Request, Session

from django_no_sql.db import errors as django_no_sql_errors
from django_no_sql.db.decorators import database_cache, database_cache_for_web

# @database_cache_for_web('this')
# def create_connection(url, method, **extra_headers):
#     session = Session()
#     headers = {}
#     headers = {**headers, **extra_headers}
#     request = Request(method=method, url=url, headers=headers)
#     prepared_request = session.prepare_request(request)
#     try:
#         response = session.send(prepared_request)
#     except:
#         pass
#     else:
#         if response.status_code == 200:
#             return response

#             def update_database(path_or_url, data_to_write, section='data'):
#     with open(_check_path(path_or_url), 'r+', encoding='utf-8') as f:
#         data = json.load(f)
#         if not data:
#             raise django_no_sql_errors.DatabaseError('The database you are '
#                                                      'trying to load contains no schema')

#         def update_schema(schema):
#             print('schema')
#             return data

#         def update_data(data):
#             print('data')
#             return data

#         if section == 'schema':
#             new_data = update_schema(data_to_write)

#         if section == 'data':
#             new_data = update_data(data_to_write)
#     return new_data


def _check_path(path_or_url):
    """
    Checks if the path of the database exists or is a url
    """
    if not path_or_url.endswith('.json'):
        raise django_no_sql_errors.DatabaseError('The file you are trying to '
                    'access is not of type JSON')

    starts_with_http = any([path_or_url.startswith('http'), \
                                path_or_url.startswith('https')])
    if starts_with_http:
        session = Session()
        with session as s:
            request = Request('GET', url=path_or_url)

            session.verify = True
            session.headers.update({})

            response = session.send(session.prepare_request(request))

            if response.status_code == 200:
                return response.json()
    else:
        path_exists = os.path.exists(path_or_url)
        if not path_exists:
            raise django_no_sql_errors.DatabaseError('The database you are trying '
                        'to open does not exist')
        return Path(path_or_url)


@functools.lru_cache
def file_reader(path_or_url, mode='r'):
    """
    Definition that opens, reads and loads the database

    Parameters
    ----------

        path_or_url: path or http/https url to the file to use
    """
    with open(_check_path(path_or_url), mode, encoding='utf-8') as db:
        try:
            raw_data = json.load(db)
        except json.JSONDecodeError:
            raise django_no_sql_errors.DatabaseError('The file you are trying to open could not be read')
        if not raw_data:
            raise django_no_sql_errors.SchemaError('The database you are trying to load is empty or does not contain a valid schema')
        return raw_data
