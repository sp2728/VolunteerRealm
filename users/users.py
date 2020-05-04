from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail_settings, db, mail
from auth.models import User, UserOrgJobs, OrgJobs

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/editUser/<id>', methods=['POST'])
@login_required
def editUser(id):
    email = request.form.get('email')
    username = request.form.get('name')
    first_name = request.form.get('FirstName')
    last_name = request.form.get('LastName')
    phone_number = request.form.get('PhoneNumber')
    linkedIn = request.form.get('linkedIn')

    user1 = User.query.filter_by(name=username).first()  # if this returns a user, then the username already exists in
    # database

    if user1:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Sorry! Username already exists')
        return redirect(url_for('user.userProfile'))

    email1 = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    # database

    if email1:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Sorry! Email already exists')
        return redirect(url_for('user.userProfile'))

    phone = User.query.filter_by(
        phone_number=phone_number).first()  # if this returns a user, then the email already exists in
    # database

    if phone:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Sorry! Phone Number already exists')
        return redirect(url_for('user.userProfile'))

    user = User.query.filter_by(id=id).first()  # if this returns a user, then the username already exists in
    # database

    user.email = email
    user.name = username
    user.first_name = first_name
    user.last_name = last_name
    user.phone_number = phone_number
    user.linkedIn = linkedIn

    db.session.commit()
    flash('Profile Updated' + user.name)
    return redirect(url_for('user.userProfile'))


@user.route('/deleteUser/<id>')
@login_required
def deleteUser(id):
    user = User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('auth.logout'))


@user.route('/userProfile')
@login_required
def userProfile():
    users = User.query.filter_by(id=current_user.id).first()
    print(id)
    return render_template('userProfile.html', users=users)


@user.route('/volunteeringHistory')
@login_required
def volunteeringHistory():
    #orgjobs = db.session.query(OrgJobs, UserOrgJobs).filter(OrgJobs.orgJob_id == UserOrgJobs.orgJob_id,
     #                                                       UserOrgJobs.id == current_user.id)
    orgjobs = db.session.query(UserOrgJobs).filter(UserOrgJobs.id == current_user.id)
    return render_template('volunteeringHistory.html', orgjobs=orgjobs)


@user.route('/opportunities')
@login_required
def opportunities():
    return redirect(url_for('main.viewOpportunities'))


@user.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@user.route('/mailAdmin', methods=['POST'])
@login_required
def mailAdmin_post():
    #email = request.form.get('email')
    email = "mmm249@njit.edu";
    #user = User.query.filter_by(email=email).first()
    msg = Message(subject="User Query",
                  sender=mail_settings["MAIL_USERNAME"],
                  recipients=[email]  # replace with your email for testing
                  )
    msg = request.form.get('comments')
    mail.send(msg)
    flash('Your message has been sent to the admin.')
