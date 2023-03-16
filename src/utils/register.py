from flask import session

def check_result_register(email, password, confirm):
    return password == confirm