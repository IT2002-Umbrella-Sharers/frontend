import requests
from .request import generate_url

def get_admin_status(email):
    url = generate_url("/isadmin")
    payload = {
        'email': email
    }
    r = requests.post(url, data=payload).json()
    try:
        return r['data'][0]['is_admin']
    except Exception as e:
        print(e)
        return False
    

def get_banned_status(email):
    url = generate_url("/isbanned")
    payload = {
        'email': email
    }
    r = requests.post(url, data=payload).json()
    try:
        return r['data'][0]['is_banned']
    except Exception as e:
        print(e)
        return False