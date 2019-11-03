from flask import render_template, url_for, flash, redirect,request
from flaskblog import app,db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, giveForm,redeemForm
from flaskblog.models import User,History
from flask_login import login_user, current_user,logout_user,login_required
from datetime import datetime

posts = [
    {
        'msg': 'Appreciate someone today!',
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password,received=0,give_balance=1000,admin=0)
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations {form.username.data}! Your account has been created ! You can login now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # to check user exists and the password entered is correct
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/give",methods=['GET', 'POST'])
@login_required
def give():
    form=giveForm()
    if form.validate_on_submit():
        if form.points.data > 0 and form.points.data<=current_user.give_balance and User.query.filter(User.email.in_(form.receiver.data)) and form.receiver.data!=current_user.email:
            flash(f'Wow! You have rewarded {form.points.data} to {form.receiver.data}!!','success')
            current_user.give_balance = current_user.give_balance - form.points.data
            db.session.commit()
            flash(f'You have {current_user.give_balance} remaining your balance to give!')
            user = User.query.filter_by(email=form.receiver.data).first()
            user.received = user.received + form.points.data
            History.amount = form.points.data
            History.r_time = datetime.utcnow
            db.session.commit()
            return redirect(url_for('give'))
        else:
            flash(f'Please enter a valid receiver or valid points', 'danger')
    return render_template('give.html', title='Give',form=form)


@app.route("/redeem",methods=['GET', 'POST'])
@login_required
def redeem():
    form=redeemForm()
    if form.validate_on_submit():
        if form.redeem_points.data>0 and form.redeem_points.data%10000==0 and form.redeem_points.data<=current_user.received:
            current_user.received = current_user.received - form.redeem_points.data
            db.session.commit()
            flash(f'You have redeemed {form.redeem_points.data} from your points! A gift voucher worth ${form.redeem_points.data/100} has been sent to your email!')
        else:
            flash(f'Please enter points as a multiple of 10000!', 'danger')
    return render_template('redeem.html', title='Redeem',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')