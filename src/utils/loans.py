from .retrieve_info import retrieve_name

def retrieve_loans(id):
    # return format is tentatively loan_id, umbrella_id, borrower_id, start_date, end_date
    r = [
        "4, 24, 7, 1/1/2023 08:00:00, 4/1/2023 06:00:00".split(", "),
        "8, 2, 1, 1/1/2023 08:00:00, 4/1/2023 06:00:00".split(", "),
        "12, 1, 4, 1/1/2023 08:00:00, 4/1/2023 06:00:00".split(", "),
        "16, 30, 6, 1/1/2023 08:00:00, 4/1/2023 06:00:00".split(", "),
        "20, 6, 9, 1/1/2023 08:00:00, 4/1/2023 06:00:00".split(", "),
    ]
    for loan in r:
        loan[2] = retrieve_name(loan[2])
    return get_loan_header() + r

def get_loan_header():
    return [["Loan ID", "Umbrella ID", "Borrower Name", "Start Date", "End Date"]]