from flask import session
from .retrieve_info import retrieve_name
from .request import get_current_loans, generate_url
import requests
import datetime

def get_umbrella(location):
    url = generate_url("getumbrella")
    payload = {
        "location": location
    }
    r = requests.post(url, data=payload).json()
    return r['data']

def submit_borrow(location):
    url = generate_url("loanumbrella")

def retrieve_borrowed(id):
    # return format is loan_id, umbrella_id, lender_name, location, start_date
    r = get_current_loans(id)
    output = []
    for loan in r:
        output.append([
            loan['loan_id'],
            loan['umbrella_id'],
            loan['first_name'] + " " + loan['last_name'],
            loan['location_name'],
            loan['start_date'] 
        ])
    return get_borrowed_header() + output

def get_borrowed_header():
    return [["Loan ID", "Umbrella ID", "Borrowed From", "Location", "Date Borrowed"]]


def borrow_umbrella(umbrellaid, borrower):
    url = generate_url("borrowumbrella")
    date = datetime.datetime.now()
    payload = {
        "umbrellaid": umbrellaid,
        "borrower": borrower,
        "date": date
    }
    r = requests.post(url, data=payload).json()
    return r['data']

def return_umbrella(loan_id, location_name):
    url = generate_url("returnumbrella")
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "loanid": loan_id,
        "date": date,
        "returnlocation": location_name
    }
    r = requests.post(url, data=payload).json()
    return r['data']