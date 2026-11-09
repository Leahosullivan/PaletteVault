# import web elements from WTF
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     IntegerField, TextAreaField)
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length, NumberRange, Optional


# create a class for the web elements needed for a Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# create a class for the web elements needed for a Register Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


# create a class for the web elements needed to log usage of a product
class UsageForm(FlaskForm):
    # InputRequired (not DataRequired) so that 0 is accepted as a valid value
    pan_progress = IntegerField('New Pan Progress (%)', validators=[
        InputRequired(message='Please enter a number between 0 and 100.'),
        NumberRange(min=0, max=100, message='Pan progress must be between 0 and 100.')])
    notes = TextAreaField('Notes (optional)', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Save Usage')
