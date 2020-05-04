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
    orgs = Organization.query.all()
    jobs = UserOrgJobs.query.filter_by(id=current_user.id).all()
    jobs_id = []
    for value in jobs:
        jobs_id += (str(value.orgJob_id))
    return render_template('viewOpportunities.html', orgJobs=orgJobs, orgs=orgs, jobs=jobs_id)


@main.route('/applyOpportunity')
@login_required
def applyOpportunityTemp():
    return render_template('applyOpportunity.html')


@main.route('/applyOpportunity/<id>')
@login_required
def applyOpportunity(id):
    job = OrgJobs.query.filter_by(orgJob_id=id).first()
    org = Organization.query.filter_by(org_id=job.org_id).first()

    jid = db.session.query(UserOrgJobs).filter(UserOrgJobs.id == current_user.id, UserOrgJobs.orgJob_id == id).first()
    if jid is None:
        ojid = UserOrgJobs(id=current_user.id, orgJob_id=id, job_title=job.job_title,
                           job_description=job.job_description, job_location=job.job_location, org_name=org.org_name)
        db.session.add(ojid)
        db.session.commit()
    else:
        flash('Already applied')
        return redirect(url_for('main.viewOpportunities'))

    msg = Message(subject="Volunteering Application",
                  sender=current_user.email,
                  recipients=[org.org_email]  # replace with your email for testing
                  )

    msg.html = render_template('/applyOpportunity.html', job=job.job_id)
    mail.send(msg)
    flash('Successfully Applied')
    return redirect(url_for('main.viewOpportunities'))


@main.route('/organizationList')
def organizationList():
    organization = Organization.query.all()
    return render_template('organizationList.html', organization=organization)

@main.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')
