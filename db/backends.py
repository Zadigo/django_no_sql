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

def _search_for_database(path):
    base, _, files = list(os.walk(path))[0]
    registry = []
    for item in files:
        if item.startswith('database') and item.endswith('json'):
            registry.append((base, item, os.path.join(base, item)))
    if len(registry) == 1:
        return registry[0]
    return registry


def _check_path(path_or_url):
    """
    Checks if the path of the database exists or is a url
    """
    if not path_or_url.endswith('.json'):
        raise django_no_sql_errors.DatabaseError('The file you are trying to access is not of type JSON')

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
            raise django_no_sql_errors.DatabaseError('The database you are trying to open does not exist')
        return Path(path_or_url)


@functools.lru_cache
def file_reader(path_or_url, mode='r', is_dir=False):
    """
    A function used to open a JSON database file

    Parameters
    ----------

        path_or_url (str): path to the file
        mode (str, optional): the default mode to open the file with. Defaults to 'r'.
        is_dir (bool, optional): whether the path is a dir. Defaults to False.

    Raises
    ------

        django_no_sql_errors.DatabaseError: [description]
        django_no_sql_errors.SchemaError: [description]

    Returns:
        [type]: [description]
    """
    if is_dir:
        path_or_url = _search_for_database(path_or_url)
    else:
        path_or_url = _check_path(path_or_url)
    if not path_or_url:
        raise django_no_sql_errors.DatabaseError('We could not find a database to open. A you sure the database exists and is at the root or your project?')
    if isinstance(path_or_url, tuple):
        path_or_url = path_or_url[2]        

    with open(path_or_url, mode, encoding='utf-8') as db:
        try:
            raw_data = json.load(db)
        except json.JSONDecodeError:
            raise django_no_sql_errors.DatabaseError('The file you are trying to open could not be read')
        if not raw_data:
            raise django_no_sql_errors.SchemaError('The database you are trying to load is empty or does not contain a valid schema')
        return raw_data
