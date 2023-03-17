from flask import session, url_for
from .loans import retrieve_loans
from .borrowed import retrieve_borrowed

def check_logged_in():
    print(session["logged_in"])
    return session["logged_in"]

def fn_login(email):
    session["logged_in"] = True
    session["email"] = email
    session["loans"] = retrieve_loans(email)
    session["borrowed"] = retrieve_borrowed(email)


def fn_logout():
    session["logged_in"] = False
    session["loans"] = []
    session["borrowed"] = []

def check_result_login(email, password):
    r = True
    if r:
        fn_login(email)
    return r

def reroute_for_login(path, other):
    if 'post' in path or "register" in path:
        return False
    if other:
        return False
    if path == url_for('login'):
        return False
    if '/static/' in path:
        return False
    return True
