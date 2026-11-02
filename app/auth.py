from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from .models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower(); password = request.form.get('password','')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password): login_user(user); return redirect(request.args.get('next') or url_for('main.dashboard'))
        flash('Invalid PhantomVault credentials.', 'error')
    return render_template('auth.html')

@auth.get('/logout')
def logout():
    logout_user(); return redirect(url_for('auth.login'))
