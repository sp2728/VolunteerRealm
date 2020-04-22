from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail_settings, mail, db

from auth.models import OrgJobs, Organization, UserOrgJobs

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/organizationList')
def organizationList():
    return render_template('organizationList.html')


@main.route('/viewOpportunities')
def viewOpportunities():
    orgJobs = OrgJobs.query.all()
    print(orgJobs)
    return render_template('viewOpportunities.html', orgJobs=orgJobs)


@main.route('/applyOpportunity/<id>')
@login_required
def applyOppurtunity(id):
    ojid = UserOrgJobs(id=current_user.id, orgJob_id=id)
    db.session.add(ojid)
    db.session.commit()

    test = 'blank mail'

    msg = Message(subject="Volunteering Application",
                  sender=current_user.email,
                  recipients=["varshaahuja13@gmail.com"],  # replace with your email for testing
                  body=test
                  )
    mail.send(msg)

    return render_template('main.viewOpportunities')
