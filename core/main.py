from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/organisationList')
def organisationList():
    return render_template('organisationList.html')


@main.route('/viewOpportunities')
def viewOpportunities():
    return render_template('viewOpportunities.html')
