import base64
import pytest
from flask import url_for
from app import db
from auth.models import User, Permission
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app


def test_index(client):
    assert client.get(url_for('main.index')).status_code == 200


def test_getLogin(client):
    assert client.get(url_for('auth.login')).status_code == 200


def test_getSignup(client):
    assert client.get(url_for('auth.signup')).status_code == 200


def test_getAboutUs(client):
    assert client.get(url_for('main.aboutUs')).status_code == 200


def test_getContact(client):
    assert client.get(url_for('user.contact')).status_code == 200


def test_login(client):
    rv = client.post(url_for('auth.login'), data={'name': 'test123', 'password': '1234'},
                     follow_redirects=True)
    assert rv.status_code == 200
    assert b"Volunteering Opportunities" in rv.data
    assert b"Contact" in rv.data
    assert b"Profile" in rv.data
    assert b"Volunteering History" in rv.data
    assert b"Logout" in rv.data
    assert b"Home" in rv.data
    return rv


def test_user_Profile(client):
    rv = test_login(client)
    rv1 = client.get(url_for('user.userProfile'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Home" in rv1.data
    assert b"Profile" in rv1.data
    assert b"Volunteering History" in rv1.data
    assert b"Volunteering Opportunities" in rv1.data
    assert b"Contact" in rv1.data
    assert b"First Name" in rv1.data
    assert b"Last Name" in rv1.data
    assert b"Email" in rv1.data
    assert b"Phone No" in rv1.data
    assert b"LinkedIn" in rv1.data
    assert b"Logout" in rv1.data
    return rv1


def test_user_volunteeringHistory(client):
    rv = test_login(client)
    rv1 = client.get(url_for('user.volunteeringHistory'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Home" in rv1.data
    assert b"Profile" in rv1.data
    assert b"Volunteering History" in rv1.data
    assert b"Volunteering Opportunities" in rv1.data
    assert b"Contact" in rv1.data
    assert b"Organization" in rv1.data
    assert b"Job Description" in rv1.data
    assert b"Location" in rv1.data
    assert b"Logout" in rv1.data
    return rv1


def test_user_volunteeringOpportunities(client):
    rv = test_login(client)
    rv1 = client.get(url_for('main.viewOpportunities'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Home" in rv1.data
    assert b"Profile" in rv1.data
    assert b"Volunteering History" in rv1.data
    assert b"Volunteering Opportunities" in rv1.data
    assert b"Contact" in rv1.data
    assert b"Organization" in rv1.data
    assert b"Job Description" in rv1.data
    assert b"Location" in rv1.data
    assert b"Logout" in rv1.data
    return rv1


def test_login_admin(client):
    rv = client.post(url_for('auth.login'), data={'name': 'varsha', 'password': '1234'},
                     follow_redirects=True)
    assert rv.status_code == 200
    assert b"Opportunities" in rv.data
    assert b"Users" in rv.data
    assert b"Organizations" in rv.data
    assert b"Dashboard" in rv.data
    assert b"Logout" in rv.data
    assert b"Home" in rv.data
    return rv


def test_admin_dashboard(client):
    rv = test_login_admin(client)
    rv1 = client.get(url_for('admin.adminDashboard'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Home" in rv1.data
    assert b"Dashboard" in rv1.data
    assert b"Logout" in rv1.data
    return rv1


def test_admin_addOpportunities(client):
    rv = test_login_admin(client)
    rv1 = client.get(url_for('admin.addOpportunity'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Job Id" in rv1.data
    assert b"Organization Name" in rv1.data
    assert b"Job Title" in rv1.data
    assert b"Job Description" in rv1.data
    assert b"Job Location" in rv1.data
    return rv1


def test_admin_addOrganization(client):
    rv = test_login_admin(client)
    rv1 = client.get(url_for('admin.addOrganization'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Organization Name" in rv1.data
    assert b"Organization Address" in rv1.data
    assert b"Email" in rv1.data
    return rv1


def test_admin_userlist(client):
    rv = test_login_admin(client)
    rv1 = client.get(url_for('admin.userList'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"User ID" in rv1.data
    assert b"User Name" in rv1.data
    assert b"User Email" in rv1.data
    assert b"Action" in rv1.data
    return rv1


def test_logout(client):
    rv = test_login(client)
    rv1 = client.get(url_for('auth.logout'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Home" in rv1.data
    assert b"Login" in rv1.data
    assert b"Sign Up" in rv1.data

@pytest.fixture(scope='function')
def user():
    _user = User(
        email='pat4@gmail.com',
        name='Pat4',
        password=generate_password_hash('xyz123', method='sha256'),
        first_name='Pat4',
        last_name='Stark1',
        phone_number='9897969586',
        gender='Male',
        linkedIn='https://www.linkedin.com/',
        permission=Permission.USER)
    db.session.add(_user)
    db.session.commit()
    yield _user
    db.session.refresh(_user)
    db.session.delete(_user)
    db.session.commit()


def test_user_creation(client):
    data={'email': 'pat@gmail.com', 'password': 'xyz123','password2': 'xyz123', 'name': 'Pat', 'FirstName': 'Pat', 'LastName': 'Stark',
            'PhoneNumber': '9897969594', 'gender': 'Male', 'linkedIn': 'https://www.linkedin.com/'}
    # dummy data creation
    rv = client.post(url_for('auth.signup'), data=data,
                     follow_redirects=True)
    assert rv.status_code == 200

    # dummy data login
    rv1 = client.post(url_for('auth.login'), data=data,
                      follow_redirects=True)
    assert rv1.status_code == 200


def test_edit(client, user):
    # edit profile
    data1= {'email': 'pat6@gmail.com', "name": user.name}
    # Authenticate client by login
    rv1 = client.post(
        url_for('auth.login'),
        data={"name": user.name, "password": "xyz123"},
        follow_redirects=True
    )

    # Call edit user end point
    rv2 = client.post(url_for('user.editUser', id=user.id), data=data1, follow_redirects=True)

    # Check if the status is 200
    assert rv2.status_code == 200

    # Refresh user object to fetch the latest object from db
    db.session.refresh(user)

    assert user.email == "pat6@gmail.com"
    assert b"Pat4" in rv2.data


@pytest.fixture(scope='function')
def user1():
        _user1 = User(
            email='pat10@gmail.com',
            name='Pat10',
            password=generate_password_hash('xyz123', method='sha256'),
            first_name='Pat10',
            last_name='Stark10',
            phone_number='9897969581',
            gender='Male',
            linkedIn='https://www.linkedin.com/',
            permission=Permission.USER
        )
        db.session.add(_user1)
        db.session.commit()
        yield _user1
        db.session.refresh(_user1)
        db.session.commit()


def test_delete(client, user1):
    # delete profile
    rv1 = client.post(url_for('auth.login'), data={'name': user1.name,'password':'xyz123'},
                      follow_redirects=True)
    assert rv1.status_code == 200

    # delete user
    rv3 = client.get(url_for('user.deleteUser', id=user1.id), follow_redirects=True)
    assert rv3.status_code == 200
