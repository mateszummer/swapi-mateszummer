import psycopg2
import psycopg2.extras
import re
from psycopg2.extensions import AsIs

import os
from urllib import parse
import psycopg2

def open_database():
    try:
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])
        connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print(exception)
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


@connection_handler
def read_all(cursor, statement, arg):
    cursor.execute(statement, arg)
    result = cursor.fetchall()
    return result

@connection_handler
def read_one(cursor, statement, arg):
    cursor.execute(statement, arg)
    result = cursor.fetchone()
    return result

@connection_handler
def write(cursor, statement, arg):
    cursor.execute(statement, arg)
