from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail_settings

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/userDashboard')
@login_required
def userDashboard():
    return render_template('userDashboard.html', name=current_user.name)


@user.route('/editUser')
@login_required
def editUser():
    return render_template('editUser.html')


@user.route('/userProfile')
@login_required
def userProfile():
    return render_template('userProfile.html')



@user.route('/volunteeringHistory')
@login_required
def volunteeringHistory():
    return redirect(url_for('main.viewOpportunities'))


@user.route('/contact')
@login_required
def contact():
    return render_template('contact.html')
