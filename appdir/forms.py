from flask_wtf import FlaskForm
# No custom variations in Flask_WTF
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from appdir.models import Patron, BankAccountType

# Define the login class using the WTForms library in Python
# This library also contains code to generate the HTML elements so we don't need to define those
# On the page
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # This method must be made in this format so WTForms knows to run it in addition to stock validators
    def validate_email(self, email):
        # find any patrons that have the same email. This is a no-no
        patrons = Patron.query.filter_by(patronEmail=email.data).first()
        if patrons is not None:
            raise ValidationError('Patron with this email already exists!')


class CreateCheckingAccountForm(FlaskForm):
    accountName = StringField('Account Name', validators=[DataRequired()])
    insurance = BooleanField('Insurance')
    submit = SubmitField('Submit', validators=[DataRequired()])


class NewAccountType(FlaskForm):
    # This *should* be pulled from the database, but it's not
    # Choices are in the format (value, display)
    choices = [('Checking', 'Checking'), ('Savings', 'Savings'), ('Retirement', 'Retirement')]
    accountChoice = RadioField(label="Select and account type", choices=choices, validators=[DataRequired()])
    submit = SubmitField(label="Open my Account")


class CreditScoreForm(FlaskForm):
    averageAge = FloatField('Average age of credit history', default=0.0)
    hardInquiries = FloatField('Hard Inquiries', default=0.0)
    creditUtilization = FloatField('Credit Utilization Percent', default=0.0)
    latePay = FloatField('Late Payments', default=0.0)
    totalAccounts = FloatField('Total Accounts', default=0.0)
    derogatoryMarks = FloatField('Derogatory Marks', default=0.0)
    submit = SubmitField('Credit Score')


class EstimateInterestForm(FlaskForm):
    choices = [('checking', 'Checking'), ('saving', 'Savings'), ('retirement', 'Retirement')]
    startingFunds = FloatField(label='Starting Funds', default=0.0)
    monthsOfInterest = FloatField(label='Years Of Interest', default=0.0)
    accountType = RadioField(label='Account Type', choices=choices)
    submit = SubmitField(label='Estimate Interest')
