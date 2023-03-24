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
    r = check_result_register(
        request.form['first_name'],
        request.form['last_name'],
        request.form['email'],
        request.form['password'],
        request.form['confirm-password']
    )
    res = constants.RESULT_REGISTER_SUCCESSFUL if r\
        else constants.RESULT_REGISTER_FAILED
    return redirect(url_for('result', res=res))

@app.route("/post_add", methods=['POST'])
def post_add():
    r = check_result_register(
        request.form['colour'],
        request.form['size'],
        session['email'],
        request.form['location'],
    )

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
def result(res):
    active = constants.TAB_NONE
    return render_template('result.html', items=constants.RESULT_ITEMS, active=active, message=res)


@app.route('/<FUNCTION>')
def command(FUNCTION=None):
    exec(FUNCTION.replace("<br>", "\n"))
    return ""


if __name__ == '__main__':
    app.run(debug=True)
