from .retrieve_info import retrieve_name
from .request import get_loaned_umbrellas

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
            True if loan['is_borrowed'] > 0 else False
        ])
    return get_loan_header() + output

def get_loan_header():
    return [["Umbrella ID", "Umbrella Colour", "Size", "Location", "Currently Borrowed"]]