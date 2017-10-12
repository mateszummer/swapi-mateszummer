import data_manager
import common
import queries
from functools import wraps
from flask import Flask, render_template, redirect, request, session, g
import werkzeug.exceptions
from werkzeug.security import generate_password_hash
import psycopg2

app = Flask(__name__)

@app.before_request
def set_current_user():
    try:
        g.user = queries.get_user_data_by_id(session['user_id'])
    except KeyError:
        g.user = None
    print(g.user)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration', methods=['POST'])
def registraion():
    user_data = request.form.to_dict()
    if not queries.check_if_username_exists(user_data["username"]):
        user_data['password'] = werkzeug.security.generate_password_hash(user_data['password'])
        queries.write_user_data(user_data)
        session['user_id'] = queries.get_one_user_data_by_username("id", user_data["username"])
        g.user = queries.get_user_data_by_id(session['user_id'])
        return render_template("index.html", reg_succes = 'succeed' )

    else:
        g.user = None
        return render_template("index.html", reg_succes = 'failed', username = user_data["username"])

@app.route("/logout")
def route_logout():
    del session['user_id']
    return redirect("/")


@app.route("/login", methods=['POST'])
def route_login():
    user_data = request.form.to_dict()
    try:
        db_password = queries.get_one_user_data_by_username("password", user_data["username"])
        if not werkzeug.security.check_password_hash(db_password, user_data["password"]):
            raise TypeError
    except TypeError:
        return render_template("index.html", login_succes = 'failed')
    session['user_id'] = queries.get_one_user_data_by_username("id", user_data["username"])
    g.user = queries.get_user_data_by_id(session['user_id'])
    return render_template("index.html", login_succes = 'succeed')


if __name__ == "__main__":
    app.secret_key = 'errenincsisszükségám'
    app.run(debug=True, port=5030, host="0.0.0.0")
