from flask import render_template, url_for, flash, redirect, request
from dateutil.relativedelta import relativedelta

from sqlalchemy.orm.sync import update

from forms import RegistrationForm, LoginForm, giveForm, redeemForm, historyForm, redemptionForm, resetForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date
import models as models


def add_app(app):
    with app.app_context():
        mw = models.ModelWrapper(app)

    @app.route("/")
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()
            # to check user exists and the password entered is correct
            if user and mw.bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                if current_user.admin == 1:
                    return redirect(next_page) if next_page else redirect(url_for('admin'))
                else:
                    return redirect(next_page) if next_page else redirect(url_for('home'))

            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form)


    @app.route("/home")
    @login_required
    def home():

        if current_user.admin==0:
            return render_template('home.html', posts=[{
                'msg': 'Appreciate someone today!',}])
        else:
            return render_template('admin.html', title='Admin')


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = mw.bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = models.User(username=form.username.data, email=form.email.data, password=hashed_password, received=0,
                           give_balance=1000, admin=0)
            models.db.session.add(user)
            models.db.session.commit()
            flash(f'Congratulations {form.username.data}! Your account has been created ! You can login now!',
                  'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)



    @app.route("/give", methods=['GET', 'POST'])
    @login_required
    def give():
        if current_user.admin == 0:
            form = giveForm()
            if form.validate_on_submit():
                if form.points.data > 0 and form.points.data <= current_user.give_balance and form.receiver.data != current_user.email \
                        and models.User.query.filter(models.User.email==form.receiver.data).count()>0 and form.receiver.data != "vrinda.sharma@utexas.edu":
                    flash(f'Wow! You have rewarded {form.points.data} to {form.receiver.data}!!', 'success')
                    current_user.give_balance = current_user.give_balance - form.points.data
                    models.db.session.commit()
                    flash(f'You have {current_user.give_balance} remaining your balance to give!')
                    user = models.User.query.filter_by(email=form.receiver.data).first()
                    user.received = user.received + form.points.data

                    hist = models.History(amount=form.points.data, r_time=datetime.utcnow(), getuser_id=user.id,
                                          senduser_id=current_user.id)
                    models.db.session.add(hist)
                    models.db.session.commit()
                    return redirect(url_for('give'))
                else:
                    flash(f'Please enter a valid receiver or valid points', 'danger')
            return render_template('give.html', title='Give', form=form)
        else:
            flash(f'Access Denied!!!', 'danger')
            return redirect(url_for('login'))

    @app.route("/redeem", methods=['GET', 'POST'])
    @login_required
    def redeem():
        if current_user.admin == 0:
            form = redeemForm()
            if form.validate_on_submit():
                if form.redeem_points.data > 0 and form.redeem_points.data % 10000 == 0 and form.redeem_points.data <= current_user.received:
                    current_user.received = current_user.received - form.redeem_points.data
                    models.db.session.commit()
                    rede = models.Redeem(amount=form.redeem_points.data, redeemtime=datetime.utcnow(), reuser_id=current_user.id)
                    models.db.session.add(rede)
                    models.db.session.commit()
                    flash(
                        f'You have redeemed {form.redeem_points.data} from your points! A gift voucher worth ${form.redeem_points.data / 100} has been sent to your email!')
                else:
                    flash(f'Please enter points as a multiple of 10000!', 'danger')
            return render_template('redeem.html', title='Redeem', form=form)
        else:
            flash(f'Access Denied!!!', 'danger')
            return redirect(url_for('login'))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route("/account")
    @login_required
    def account():
        return render_template('account.html', title='Account')

    @app.route("/history")
    @login_required
    def history():
        if current_user.admin == 0:

            events = models.Redeem.query.with_entities(models.Redeem.amount, models.Redeem.redeemtime).filter(models.Redeem.reuser_id==current_user.id).order_by(models.Redeem.redeemtime).all()

            events1 = models.History.query.with_entities(models.History.id, models.History.amount, models.History.r_time,
                                                        models.History.senduser_id,
                                                        models.History.getuser_id).filter(models.History.senduser_id==current_user.id).all()

            events2 = models.History.query.with_entities(models.History.id, models.History.amount,
                                                         models.History.r_time,
                                                         models.History.senduser_id,
                                                         models.History.getuser_id).filter(
                models.History.getuser_id == current_user.id).all()

            return render_template('history.html', title='Redemption History', events=events, sends=events1, gets = events2)

    @app.route("/admin")
    @login_required
    def admin():
        if current_user.admin == 1:
            return render_template('admin.html', title='Admin')

    @app.route("/tranhis")
    @login_required
    def tranhis():
        events = models.History.query.with_entities(models.History.id, models.History.amount, models.History.r_time, models.History.senduser_id,
                                      models.History.getuser_id).order_by(models.History.id).all()
        return render_template('tranhis.html', title='Transaction History', events=events)


    @app.route("/reset", methods=['GET', 'POST'])
    @login_required
    def reset():
        form=resetForm()
        if form.validate_on_submit():

            models.User.query. \
                filter(models.User.admin == 0). \
                update({"give_balance": (1000)})

            models.db.session.commit()
            flash(f'You have reset the gift balance of all the employees!', 'success')
        return render_template('reset.html', title='Reset',form=form)

    @app.route("/userrank")
    @login_required
    def userrank():
        events = models.User.query.with_entities(models.User.id, models.User.username, models.User.email, models.User.received).filter(models.User.admin==0).order_by(
            models.User.received.desc()).all()
        return render_template('userrank.html', title='User Ranking', events=events)

    @app.route("/userwithcredit")
    @login_required
    def userwithcredit():
        events = models.User.query.with_entities(models.User.id, models.User.username, models.User.email, models.User.give_balance).filter(models.User.give_balance!=0).order_by(models.User.id).all()
        return render_template('userwithcredit.html', title='Credit Left', events=events)



    @app.route("/redemption", methods=['POST','GET'])
    @login_required
    def redemption():
        # select='This Month'
        # id = 4

        form = redemptionForm()
        select = str(form.comp_select.data)
        id = form.userid.data
        # flash(select)
        if request.method=='POST' and form.comp_select.data=='This Month':
            if form.validate_on_submit() :

                flash(f'{select}, {id}', 'success')
            return redirect(url_for('rethis', id=id))
        elif request.method=='POST' and form.comp_select.data=='Last Month':
            if form.validate_on_submit() :

                flash(f'{select}, {id}', 'success')
            return redirect(url_for('relast', id=id))

        return render_template('redemption.html', title='Redemption', form=form)

    @app.route('/rethis?id=<id>')
    def rethis(id):
        date1 = date.today()
        datemonth = str(date1)[0:7]
        events = models.Redeem.query.filter(models.Redeem.redeemtime.like(datemonth + "%")).filter(
            models.Redeem.reuser_id == id).all()
        return render_template('rethis.html', title='redemption', events=events)

    @app.route('/relast?id=<id>')
    def relast(id):
        date1 = date.today()
        date2 = date1 + relativedelta(months=-1)
        datemonth = str(date2)[0:7]
        events = models.Redeem.query.filter(models.Redeem.redeemtime.like(datemonth + "%")).filter(
            models.Redeem.reuser_id == id).all()
        return render_template('relast.html', title='redemption', events=events)