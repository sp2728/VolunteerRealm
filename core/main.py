from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/organizationList')
def organizationList():
    return render_template('organizationList.html')


@main.route('/viewOpportunities')
def viewOpportunities():
    return render_template('viewOpportunities.html')
