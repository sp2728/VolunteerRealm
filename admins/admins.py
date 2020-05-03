from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, admin_only
from auth.models import Organization, OrgJobs, User

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/adminDashboard')
@login_required
@admin_only
def adminDashboard():
    return render_template('adminDashboard.html', first_name=current_user.first_name)


@admin.route('/usersLists')
@login_required
@admin_only
def userList():
    user = User.query.all()
    return render_template('userList.html', user=user)

@admin.route('/deleteUser')
@login_required
@admin_only
def deleteUser():
    return render_template('userList.html')


@admin.route('/addOrganization')
@login_required
@admin_only
def addOrganization():
    return render_template('addOrganization.html')


@admin.route('/addOrganization', methods=['POST'])
@login_required
@admin_only
def addOrganization_post():
    organizationName = request.form.get('organizationName')
    organizationAddress = request.form.get('organizationAddress')
    organizationEmail = request.form.get('email')

    org_name = Organization.query.filter_by(org_name=organizationName).first()
    if org_name:
        flash('Organization is already exists')
        return redirect(url_for('admin.addOrganization'))

    new_org = Organization(org_name=organizationName, org_address=organizationAddress, org_email=organizationEmail)
    db.session.add(new_org)
    db.session.commit()
    return redirect(url_for('main.organizationList'))


@admin.route('/addOpportunity')
@login_required
@admin_only
def addOpportunity():
    orgName = Organization.query.all()
    return render_template('addOpportunity.html', orgName=orgName)


@admin.route('/addOpportunity', methods=['POST'])
@login_required
@admin_only
def addOpportunity_post():
    jobId = request.form.get('jobId')
    orgNm = request.form.get('orgNm')
    jobTitle = request.form.get('jobTitle')
    jobDescription = request.form.get('jobDescription')
    jobLocation = request.form.get('jobLocation')

    jid = OrgJobs.query.filter_by(job_id=jobId).first()

    if jid:
        flash('Job Id already exists')
        return redirect(url_for('admin.addOpportunity'))


    orgId = db.session.query(Organization.org_id).filter(Organization.org_name == orgNm).first()[0]

    new_job = OrgJobs(job_id=jobId, org_id=orgId, job_title=jobTitle, job_description=jobDescription,
                      job_location=jobLocation)
    db.session.add(new_job)
    db.session.commit()
    return redirect(url_for('main.viewOpportunities'))


@admin.route('/editOrganization/<id>')
@login_required
@admin_only
def editOrganization(id):
    org = Organization.query.filter_by(org_id=id).first()

    return render_template('addOrganization.html', org=org, edit=1)

@admin.route('/editOrganization/<id>',  methods=['POST'])
@login_required
@admin_only
def editOrganization_post(id):
    organizationName = request.form.get('organizationName')
    organizationAddress = request.form.get('organizationAddress')
    organizationEmail = request.form.get('email')

    org = Organization.query.filter_by(org_id=id).first()
    org.org_name=organizationName;
    org.org_address=organizationAddress;
    org.org_email=organizationEmail
    db.session.commit()
    flash('Organisation Updated'+ org.org_name)
    return redirect(url_for('main.organizationList'))


@admin.route('/deleteOrganization/<id>')
@login_required
@admin_only
def deleteOrganization(id):
    org = Organization.query.filter(Organization.org_id==id).delete()
    db.session.commit()

    return redirect(url_for('main.organizationList'))

