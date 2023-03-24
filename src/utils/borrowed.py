from flask import session
from .retrieve_info import retrieve_name
from .request import get_current_loans

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