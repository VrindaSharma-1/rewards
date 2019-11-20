from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User,History

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username already exists! Choose another!')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email already exists! Choose another!')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class giveForm(FlaskForm):
    points = IntegerField('Reward Points',validators=[DataRequired()])
    receiver = StringField('Receiver Email', [DataRequired(), Email()])
    submit = SubmitField('Give')

class redeemForm(FlaskForm):
    redeem_points = IntegerField('Redeem Points',validators=[DataRequired()])
    # receiver = StringField('ReceiverEmail', [DataRequired(), Email()])

    submit = SubmitField('Redeem')

class historyForm(FlaskForm):

    submit = SubmitField('Back To Home')

class resetForm(FlaskForm):

    submit = SubmitField('Reset')


# class redemptionForm(FlaskForm):
#     userid = IntegerField('User ID', validators=[DataRequired()])
#     month = SelectField('Month', validators=[DataRequired()],choices=[('This Month','This Month'),('Last Month','Last Month')])
#     submit = SubmitField('Redemption')

# class redemptionForm(FlaskForm):
#     userid = IntegerField('User ID', validators=[DataRequired()])
#     submit = SubmitField('Redemption')

class redemptionForm(FlaskForm):
    comp_select = StringField('comp_select',validators=[DataRequired()])
    userid = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Redemption')