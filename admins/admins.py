from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, admin_only
from auth.models import Organisation

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

@admin.route('/addOrganisation')
@login_required
@admin_only
def addOrganisation():
    return render_template('addOrganisation.html')

@admin.route('/addOrganisation', methods=['POST'])
@login_required
@admin_only
def addOrganisation_post():
    organisationName = request.form.get('organisationName')
    organisationAddress = request.form.get('organisationAddress')
    print(organisationName,organisationAddress)

    org_name = Organisation.query.filter_by(org_name=organisationName).first()
    if org_name:
        flash('Organisation is already exists')
        print('hel')
        return redirect(url_for('admin.addOrganisation'))

    new_org= Organisation(org_name=organisationName,org_address=organisationAddress)
    db.session.add(new_org)
    db.session.commit()
    return redirect(url_for('main.organisationList'))

@admin.route('/addOppurtunity')
@login_required
@admin_only
def addOppurtunity():
    return render_template('addOppurtunity.html')

@admin.route('/addOppurtunity', methods=['POST'])
@login_required
@admin_only
def addOppurtunity_post():
    jobTitle = request.form.get('jobTitle')
    jobDescription = request.form.get('jobDescription')
    print(jobTitle,jobDescription)

    new_org= Organisation(job_title=jobTitle,job_description=jobDescription)
    db.session.add(new_org)
    db.session.commit()
    return redirect(url_for('main.viewOpportunities'))

@admin.route('/updateOrganisation')
@login_required
@admin_only
def updateOrganisation():
    return render_template('organisationList.html')

@admin.route('/deleteOrganisation')
@login_required
@admin_only
def deleteOrganisation():

    return render_template('organisationList.html')
