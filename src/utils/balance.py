import requests
from flask import session
from .request import generate_url

def get_balance(email):
    url = generate_url('/getbalance')
    payload = {
        'id': email
    }
    r = requests.post(url, data=payload).json()
    if r['data']:
        return r['data'][0]['balance']
    else:
        return 0

def add_balance(email, amount):
    url = generate_url('/addbalance')
    payload = {
        'id': email,
        'amount': amount
    }
    r = requests.post(url, data=payload).json()
    return r['data']