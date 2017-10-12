import data_manager
import common
import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs

def write_user_data(user_data):
    statement = """
        INSERT INTO users
        (username, password)
        VALUES (%(username)s , %(password)s)"""
    arg = {
        'username': user_data['username'],
        'password': user_data['password']
    }
    data_manager.write(statement, arg)


def get_user_data_by_id(user_id):
    statement = """
        SELECT * FROM users WHERE id = %(user_id)s"""
    arg = {
        'user_id': user_id
    }
    return data_manager.read_one(statement, arg)

def get_one_user_data_by_username(column, username):
    statement = """
        SELECT %(column)s FROM users
        WHERE username = %(username)s"""
    arg = {
        'column': AsIs(column),
        'username': username
    }
    return data_manager.read_one(statement, arg)[column]

def check_if_username_exists(username):
    statement = """
        SELECT 1 FROM users
        WHERE username = %(username)s"""
    arg = {
        'username': username
    }
    return True if data_manager.read_one(statement, arg) else False
