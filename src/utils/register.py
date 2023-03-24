from flask import session
from .request import register
from .login import fn_login

def check_result_register(first_name, last_name, email, password, confirm):
    if password != confirm:
        session['invalid_register'] = True
        return False
    r = register(email, password, first_name, last_name)
    if r:
        session['invalid_register'] = False
    else:
        fn_login(email)
    return r
