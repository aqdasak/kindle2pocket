from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import check_password_hash

from kindle2pocket.extensions import db
from kindle2pocket.models import User

# from kindle2pocket.config import params

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    login_email = request.form.get('login_email')
    login_password = request.form.get('login_pass')

    signup_email = request.form.get('signup_email')
    signup_password1 = request.form.get('signup_pass1')
    signup_password2 = request.form.get('signup_pass2')

    if login_email:
        login_email = login_email.lower()
        user = User.query.filter_by(email=login_email).first()

        if user and check_password_hash(user.password, login_password):
            session['user'] = login_email
        else:
            flash('Could not login. Please check and try again.')

    elif signup_email:
        signup_email = signup_email.lower()
        # checking against existing email
        if User.query.filter_by(email=signup_email).first():
            flash('Email already registered', 'danger')
        else:
            if signup_password1 == signup_password2:
                user = User(email=signup_email, password=signup_password1)
                db.session.add(user)
                db.session.commit()

                # TO DO flash in html and dashboard change checking
                flash("Sign up completed", "success")
                # signing in
                session['user'] = signup_email

                return redirect(url_for('main.index'))
            else:
                flash('Wrong values entered', "danger")

    # when user login after adding url
    if 'item_url' in session and 'user' in session:
        print('\n\n\n'+session['item_url']+'\n\n\n')
        return redirect(url_for('main.add', item_url=session['item_url']))

    return redirect(url_for('main.index'))


@auth.route('/logout/')
def logout():
    # session.pop('user')
    session.clear()
    return redirect(url_for('main.index'))

#
# @auth.route('/change-pass/', methods=['GET', 'POST'])
# def change_pass():
#     if 'user' in session:
#         user = User.query.filter_by(email=session['user']).first()
#         if request.method == 'POST':
#
#             current_password = request.form.get('current_password')
#             new_password1 = request.form.get('new_password1')
#             new_password2 = request.form.get('new_password2')
#             if check_password_hash(user.password, current_password):
#                 if new_password1 == new_password2:
#                     user.password = new_password1
#                     db.session.commit()
#                     flash("Password changed successfully", "success")
#                 else:
#                     flash("Password didn't match", "danger")
#
#             else:
#                 flash('Current password is wrong', 'danger')
#
#         return render_template('change_pass.html', user=user)
#
#     return redirect(url_for('main.index'))
#
#
# @auth.route('/reset-pass/', methods=['GET', 'POST'])
# def reset_pass():
#     if request.method == 'POST':
#
#         otp = int(request.form.get('otp'))
#
#         username = request.form.get('username')
#         new_password1 = request.form.get('new_password1')
#         new_password2 = request.form.get('new_password2')
#
#         user = User.query.filter_by(username=username).first()
#
#         if otp == session['otp']:
#             session.pop('otp')
#             if new_password1 == new_password2:
#                 user.password = new_password1
#                 db.session.commit()
#                 flash("Password changed successfully", "success")
#             else:
#                 flash("Password didn't match", "danger")
#
#         else:
#             flash('OTP is wrong', 'danger')
#         return redirect(url_for('auth.login'))
#
#
# @auth.route('/reset_pass_otp', methods=['GET', 'POST'])
# def reset_pass_otp():
#     if request.method == 'POST':
#
#         username = request.form.get('username')
#         if username:
#             user = User.query.filter_by(username=username).first()
#         else:
#             email = request.form.get('email')
#             user = User.query.filter_by(email=email).first()
#         if not user:
#             flash(r"Username/email not found", 'danger')
#             return render_template('forgot_pass/send_otp.html')
#
#         from random import randint
#         session['otp'] = randint(100000, 999999)
#
#         mail.send_message('Password reset: Coderg',
#                           sender='noreply.coderg@gmail.com',
#                           recipients=[user.email],
#                           body=f'Hi {user.fullname},\n\n'
#                                f'You recently requested to reset your password for Coderg account.\n'
#                                f'This is your otp for password resetting\n{session["otp"]}\n\n'
#                                f'If you did not request a password reset, please ignore this email.\n\n'
#                                f'Thanks\nCoderg Developers\n{params["website_url"]}')
#
#         return render_template('forgot_pass/reset_pass.html', username=user.username)
#
#     return render_template('forgot_pass/send_otp.html')
