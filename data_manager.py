from config import Config
import psycopg2
import psycopg2.extras
import re
from psycopg2.extensions import AsIs


def open_database():
    try:
        connection_string = Config.DB_CONNECTION_STR
        connection = psycopg2.connect(connection_string)
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
