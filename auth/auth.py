from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from auth.models import User, Permission
from app import db, mail_settings, mail
from flask_mail import Message

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/forgotUsername')
def forgotUsername():
    return render_template('forgotUsername.html')


@auth.route('/forgotUsername' , methods=['POST'])
def forgotUsername_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    test ="Your account username is"+ user.name
    if user:
        msg = Message(subject="Hello",
                  sender=mail_settings["MAIL_USERNAME"],
                  recipients=[email],  # replace with your email for testing
                  body=test
                      )
        mail.send(msg)

        flash('Reset link has been sent to your Email Id.')
        return redirect(url_for('auth.login'))
    else:
        flash('Email Id is invalid')
        return redirect(url_for('auth.forgotUsername'))

@auth.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPassword.html')

@auth.route('/forgotPassword' , methods=['POST'])
def forgotPassword_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    test ="Please reset your password using the following link"+ 'http://127.0.0.1:5000/resetPassword/'+ str(user.id)
    if user:
        msg = Message(subject="Hello",
                  sender=mail_settings["MAIL_USERNAME"],
                  recipients=[email],  # replace with your email for testing
                  body=test
                      )
        mail.send(msg)

        flash('Reset link has been sent to your Email Id.')
        return redirect(url_for('auth.login'))
    else:
        flash('Email Id is invalid')
        return redirect(url_for('auth.forgotPassword'))

@auth.route('/resetPassword/<id>')
def resetPassword(id):
    return render_template('resetPassword.html', id=id)

@auth.route('/resetPassword',methods=['POST'])
def resetPassword_post():
    newPassword=request.form.get('newPassword')
    confirmPassword=request.form.get('confirmPassword')
    id= request.form.get('id')
    if(newPassword!=confirmPassword):
        flash('Both the passwords should be same')
        return render_template('resetPassword.html', id=id)

    else:
        user = User.query.filter_by(id=id).first()
        user.password= generate_password_hash(confirmPassword,method='sha256')
        return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    first_name = request.form.get('FirstName')
    last_name = request.form.get('LastName')
    phone_number = request.form.get('PhoneNumber')
    gender = request.form.get('gender')
    
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email,name=name,password=generate_password_hash(password,method='sha256'),first_name=first_name,last_name=last_name,phone_number=phone_number,gender=gender,permission=Permission.USER)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
