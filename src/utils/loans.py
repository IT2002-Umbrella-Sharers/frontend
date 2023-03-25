from .retrieve_info import retrieve_name
from .request import get_loaned_umbrellas, generate_url
import requests

def submit_loan(id, size, colour, location):
    url = generate_url("/loanumbrella")
    payload = {
        "email": id,
        "size": size,
        "colour": colour,
        "location": location
    }
    r = requests.post(url, data=payload).json()
    print("r: ", r)
    return r['data']

def retrieve_loans(id):
    # return format is tentatively loan_id, umbrella_id, borrower_id, start_date, end_date
    r = get_loaned_umbrellas(id)
    output = []
    for loan in r:
        output.append([
            loan['id'],
            loan['colour'],
            loan['size'],
            loan['location'],
            loan['exists']
        ])
    return get_loan_header() + output

def get_loan_header():
    return [["Umbrella ID", "Umbrella Colour", "Size", "Location", "Currently Borrowed"]]