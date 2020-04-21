from flask import Blueprint, render_template
from flask_login import login_required

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/userDashboard')
@login_required
def userDashboard():
    return render_template('userDashboard.html')

@user.route('/editUser')
@login_required
def editUser():
    return render_template('editUser.html')

@user.route('/userProfile')
@login_required
def userProfile():
    return render_template('userProfile.html')

@user.route('/applyOpportunity')
@login_required
def applyOppurtunity():
    return render_template('applyOpportunity.html')

@user.route('/volunteeringHistory')
@login_required
def volunteeringHistory():
    return render_template('volunteeringHistory.html')

@user.route('/contact')
@login_required
def contact():
    return render_template('contact.html')
