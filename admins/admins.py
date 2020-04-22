from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, admin_only
from auth.models import Organization, OrgJobs

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
    return render_template('userList.html')


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
    print(organizationName, organizationAddress)

    org_name = Organization.query.filter_by(org_name=organizationName).first()
    if org_name:
        flash('Organization is already exists')
        return redirect(url_for('admin.addOrganization'))

    new_org = Organization(org_name=organizationName, org_address=organizationAddress)
    db.session.add(new_org)
    db.session.commit()
    return redirect(url_for('main.organizationList'))


@admin.route('/addOpportunity')
@login_required
@admin_only
def addOpportunity():
    return render_template('addOpportunity.html')


@admin.route('/addOpportunity', methods=['POST'])
@login_required
@admin_only
def addOpportunity_post():
    jobId = request.form.get('jobId')
    orgId = request.form.get('orgId')
    jobTitle = request.form.get('jobTitle')
    jobDescription = request.form.get('jobDescription')
    jobLocation = request.form.get('jobLocation')
    print(jobTitle, jobDescription)

    opporgId = Organization.query.filter_by(org_id=orgId).first()

    if opporgId:
        new_job = OrgJobs(job_id=jobId, org_id=orgId, job_title=jobTitle, job_description=jobDescription,
                          job_location=jobLocation)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('main.viewOpportunities'))
    else:
        flash('Invalid Organization Id')
        return redirect(url_for('admin.addOpportunity'))



@admin.route('/updateOrganization')
@login_required
@admin_only
def updateOrganization():
    return render_template('organizationList.html')


@admin.route('/deleteOrganization')
@login_required
@admin_only
def deleteOrganization():
    return render_template('organizationList.html')
