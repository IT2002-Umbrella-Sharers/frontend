from flask import session, url_for
from .loans import retrieve_loans
from .borrowed import retrieve_borrowed
from .request import check_credentials, get_locations

def check_logged_in():
    return session["logged_in"]

def fn_login(email):
    session["logged_in"] = True
    session["email"] = email
    session["loans"] = retrieve_loans(email)
    session["borrowed"] = retrieve_borrowed(email)
    session["locations"] = get_locations()
    session["incorrect_input"] = False
    session["invalid_register"] = False
    session['available_umbrella'] = []

def fn_logout():
    session["logged_in"] = False
    session["incorrect_input"] = False
    session["invalid_register"] = False
    session['available_umbrella'] = []

def check_result_login(email, password):
    r = check_credentials(email, password)
    if r:
        fn_login(email)
    else:
        session["incorrect_input"] = True
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
