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

@user.route('/deleteUser')
@login_required
def deleteUser():
    return render_template('userList.html')

@user.route('/applyOppurtunity')
@login_required
def applyOppurtunity():
    return render_template('applyOppurtunity.html')