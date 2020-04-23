from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
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
    username = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('admin.adminDashboard'))


@auth.route('/forgotUsername')
def forgotUsername():
    return render_template('forgotUsername.html')


@auth.route('/forgotUsername', methods=['POST'])
def forgotUsername_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        msg = Message(subject="Forgot Username",
                      sender=mail_settings["MAIL_USERNAME"],
                      recipients=[email]  # replace with your email for testing
                      )
        msg.html = '''<p>Hello {},</p> 
                <p>You or someone else has requested to know the username for your account.</p> 
                <p> Your username is <strong> {}</strong>.</p>
                <p>If you did not make this request, then you can simply ignore this email.</p>

                <p>Best Wishes,</p>
                <p>Admin</p>
                <p>Admin@volunteerrealm.com</p>'''.format(user.first_name, user.name)
        mail.send(msg)

        flash('Your Username has been sent to your Email Id.')
        return redirect(url_for('auth.login'))
    else:
        flash('Email Id is invalid')
        return redirect(url_for('auth.forgotUsername'))


@auth.route('/forgotPassword')
def forgotPassword():
    return render_template('forgotPassword.html')


@auth.route('/forgotPassword', methods=['POST'])
def forgotPassword_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    link = 'http://127.0.0.1:5000/resetPassword/' + str(user.id)
    if user:
        msg = Message(subject="Password Reset Link",
                      sender=mail_settings["MAIL_USERNAME"],
                      recipients=[email]  # replace with your email for testing
                      )
        msg.html = '''<p>Hello {},</p> 
        <p>You or someone else has requested that a new password be generated for your 
        account. If you made this request,then please click this link: <a href={}><strong>reset 
        password</strong></a>. If you did not make this request, then you can simply ignore this email.</p> 
        
        <p>Best Wishes,</p>
        <p>Admin</p>
        <p>Admin@volunteerrealm.com</p>'''.format(user.first_name, link)
        mail.send(msg)

        flash('Reset link has been sent to your Email Id.')
        return redirect(url_for('auth.login'))
    else:
        flash('Email Id is invalid')
        return redirect(url_for('auth.forgotPassword'))


@auth.route('/resetPassword/<id>')
def resetPassword(id):
    return render_template('resetPassword.html', id=id)


@auth.route('/resetPassword', methods=['POST'])
def resetPassword_post():
    newPassword = request.form.get('newPassword')
    confirmPassword = request.form.get('confirmPassword')
    id = request.form.get('id')
    print(id)
    if newPassword != confirmPassword:
        flash('Both the passwords should be same')
        return render_template('resetPassword.html', id=id)

    else:
        user = User.query.filter_by(id=id).first()
        user.password = generate_password_hash(confirmPassword, method='sha256')
        db.session.commit()
        return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    first_name = request.form.get('FirstName')
    last_name = request.form.get('LastName')
    phone_number = request.form.get('PhoneNumber')
    linkedIn = request.form.get('linkedIn')
    gender = request.form.get('gender')

    user = User.query.filter_by(name=username).first()  # if this returns a user, then the username already exists in
    # database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Sorry! Username already exists')
        return redirect(url_for('auth.signup'))

    email1 = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    # database

    if email1:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Sorry! Email already exists')
        return redirect(url_for('auth.signup'))

    phone = User.query.filter_by(phone_number=phone_number).first()  # if this returns a user, then the email already exists in
    # database

    if phone:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Sorry! Phone Number already exists')
        return redirect(url_for('auth.signup'))

    if password2 != password:  # if password & confirm password does not match then we want to redirect to signup page
        # so user can update the same
        flash('Password and Confirm Password does not match')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=username, password=generate_password_hash(password, method='sha256'),
                    first_name=first_name, last_name=last_name, phone_number=phone_number, gender=gender, linkedIn=linkedIn,
                    permission=Permission.USER)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
