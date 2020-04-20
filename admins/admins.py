from flask import Blueprint, render_template
from flask_login import login_required
from app import db

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/adminDashboard')
@login_required
def adminDashboard():
    return render_template('adminDashboard.html')

@admin.route('/usersLists')
@login_required
def userList():
    return render_template('userList.html')

@admin.route('/deleteUser')
@login_required
def deleteUser():
    return render_template('userList.html')

@admin.route('/addOrganisation')
@login_required
def addOrganisation():
    return render_template('addOrganisationList.html')

@admin.route('/updateOrganisation')
@login_required
def updateOrganisation():
    return render_template('organisationList.html')

@admin.route('/deleteOrganisation')
@login_required
def deleteOrganisation():
    return render_template('organisationList.html')
