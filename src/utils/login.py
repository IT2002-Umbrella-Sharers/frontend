from flask import session, url_for
from .loans import retrieve_loans
from .borrowed import retrieve_borrowed
from .balance import get_balance
from .request import check_credentials, get_locations
from .users import get_admin_status, get_banned_status
from .admin import get_users

def check_logged_in():
    if 'logged_in' not in session:
        fn_logout()
    return session["logged_in"]

def fn_login(email):
    session["logged_in"] = True
    session["email"] = email
    session["loans"] = retrieve_loans(email)
    session["borrowed"] = retrieve_borrowed(email)
    session["locations"] = get_locations()
    session["balance"] = get_balance(email)
    session["incorrect_input"] = False
    session["invalid_register"] = False
    session['available_umbrella'] = []
    session['is_admin'] = get_admin_status(email)
    if session['is_admin']:
        for user in get_users():
            session['all_users'].append([
                user['email_address'],
                user['name'],
                user['is_banned'],
            ])

def fn_logout():
    session["logged_in"] = False
    session["incorrect_input"] = False
    session["invalid_register"] = False
    session['available_umbrella'] = []
    session['is_admin'] = False
    session['all_users'] = [['Email Address', 'Name', 'Is Banned']]

def check_result_login(email, password):
    valid_user = check_credentials(email, password)
    if valid_user:
        fn_login(email)
    else:
        session["incorrect_input"] = True
    
    session['is_banned'] = get_banned_status(email)

    return (valid_user and not(session['is_banned']))

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
