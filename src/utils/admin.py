import requests
from .request import generate_url

def get_users():
    url = generate_url('/getusers')
    res = requests.get(url).json()
    return res['data']

def post_ban(email):
    url = generate_url('/ban')
    payload = {
        'email': email
    }
    res = requests.post(url, data=payload).json()
    return res['data']

def post_unban(email):
    url = generate_url('/unban')
    payload = {
        'email': email
    }
    res = requests.post(url, data=payload).json()
    return res['data']