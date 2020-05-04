import pytest
from flask import url_for
from app import db
from auth.models import User
from flask_login import login_required, current_user
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


def test_logout(client):
    rv = test_login(client)
    rv1 = client.get(url_for('auth.logout'), follow_redirects=True)
    assert rv1.status_code == 200
    assert b"Home" in rv1.data
    assert b"Login" in rv1.data
    assert b"Sign Up" in rv1.data


def test_user_creation(client):
    # dummy data creation
    data = {'email': 'pat@gmail.com', 'password': 'xyz123', 'name': 'Pat', 'first_name': 'Pat', 'last_name': 'Stark', 'phone_number': '9897969594', 'gender': 'Male', 'linkedIn': 'https://www.linkedin.com/' }
    rv = client.post(url_for('auth.signup'), data=data,
                     follow_redirects=True)
    assert rv.status_code == 200
    # dummy data login
    rv1 = client.post(url_for('auth.login'), data=data,
                      follow_redirects=True)
    assert rv1.status_code == 200
