from flask import Flask, render_template, session
from flask_session import Session
import constants.index as constants
from utils.main import *

app = Flask(__name__, template_folder='html', static_folder='static')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.context_processor
def inject_user():
    return dict(constants=constants, session=session, login=fn_login, logout=fn_logout)


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


@app.route('/user')
def user():
    active = constants.TAB_NONE
    return render_template('user.html', items=constants.USER_ITEMS, active=active)


@app.route('/admin')
def admin():
    active = constants.TAB_NONE
    return render_template('admin.html', items=constants.ADMIN_ITEMS, active=active)


@app.route('/<FUNCTION>')
def command(FUNCTION=None):
    exec(FUNCTION.replace("<br>", "\n"))
    return ""


if __name__ == '__main__':
    app.run(debug=True)
