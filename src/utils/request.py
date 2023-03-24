import requests

BASE_URL = "http://127.0.0.1:7777"

# Helper Function
def generate_url(route):
    return BASE_URL + "/" + route

# Get Requests
def get_locations():
    url = generate_url("getlocations")
    r = requests.get(url).json()
    locations = []
    for location in r['data']:
        locations.append(location['name'])
    return locations

# Post Requests
def check_credentials(email, password):
    url = generate_url("login")
    payload = {
        'email': email,
        'password': password
    }
    r = requests.post(url, data=payload).json()
    return r['data']

def get_name(email):
    url = generate_url("names")
    payload = {
        'email': email
    }
    r = requests.post(url, data=payload).json()
    if not(r['data']):
        return []
    return r['data']

def get_current_loans(email):
    url = generate_url("getborrows")
    payload = {
        'email': email
    }
    r = requests.post(url, data=payload).json()
    if not(r['data']):
        return []
    return r['data']

def get_loaned_umbrellas(email):
    url = generate_url("getloans")
    payload = {
        'email': email
    }
    r = requests.post(url, data=payload).json()
    if not(r['data']):
        return []
    return r['data']

def register(email, password, first_name, last_name):
    url = generate_url("register")
    payload = {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    }
    r = requests.post(url, data=payload).json()
    print(r)
    return r['data']

def return_umbrella(loan_id):
    url = generate_url("loans")
    payload = {
        'email': loan_id
    }
    r = requests.post(url, data=payload).json()
    if not(r['data']):
        return []
    return r['data']

def top_up(email, amount):
    amount = min(amount, 0)
    url = generate_url("topup")
    payload = {
        'email': email,
        'amount': amount
    }
    r = requests.post(url, data=payload).json()
    if not(r['data']):
        return []
    return r['data']