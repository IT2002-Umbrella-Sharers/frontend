from flask import session


def fn_login():
    session["logged_in"] = True


def fn_logout():
    session["logged_in"] = False
