import data_manager
import bcrypt
import re
import queries


def hash_pw(password):
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def check_password(plain_text_password, hashed_text_password):
    hashed_bytes_password = hashed_text_password.encode("utf-8")
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def reg_data_checker(user_data, message=None):
    if queries.check_if_item_exist(user_data['email'], 'email', 'users') is True:
        message = 'This email already exists'
    elif queries.check_if_item_exist(user_data['nickname'], 'nickname', 'users') is True:
        message = 'This nickname already exists'
    elif user_data['password1'] != user_data['password2']:
        message = 'The passwords you have entered do not match'
    return message


def check_login(login_data):
    error_message = ""
    if queries.check_if_item_exist(login_data["email"], "email", "users") is False:
        error_message = "This user does not exist!"
        return error_message
    if check_password(
            login_data["password"],
            queries.get_one_user_inf_by_email('password', login_data["email"])) is False:
        error_message = "The password is not correct!"
        return error_message
