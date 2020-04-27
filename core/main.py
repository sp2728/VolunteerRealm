from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail_settings, mail, db

from auth.models import OrgJobs, Organization, UserOrgJobs

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/viewOpportunities')
def viewOpportunities():
    orgJobs = OrgJobs.query.all()
    return render_template('viewOpportunities.html', orgJobs=orgJobs)


@main.route('/applyOpportunity')
@login_required
def applyOppurtunityTemp():
    return render_template('applyOpportunity.html')


@main.route('/applyOpportunity/<id>')
@login_required
def applyOppurtunity(id):
    jid = db.session.query(UserOrgJobs).filter(UserOrgJobs.id==current_user.id, UserOrgJobs.orgJob_id==id).first()
    if jid is None:
        ojid = UserOrgJobs(id=current_user.id, orgJob_id=id)
        db.session.add(ojid)
        db.session.commit()
    else:
        flash('Already applied')
        return redirect(url_for('main.viewOpportunities'))

    job = OrgJobs.query.filter_by(orgJob_id=id).first()
    org = Organization.query.filter_by(org_id=job.org_id).first()

    msg = Message(subject="Volunteering Application",
                  sender=current_user.email,
                  recipients=[org.org_email]  # replace with your email for testing
                  )

    msg.html = render_template('/applyOpportunity.html', job=job.job_id)
    mail.send(msg)
    flash('Successfully Applied')
    return redirect(url_for('main.viewOpportunities'))


@main.route('/organizationList')
@login_required
def organizationList():
    organization = Organization.query.all()
    return render_template('organizationList.html', organization=organization)
