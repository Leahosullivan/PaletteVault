# import date to check the opened date is not in the future
from datetime import date

# import web elements from WTF
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     SelectField, DateField, IntegerField)
from wtforms.validators import (DataRequired, EqualTo, InputRequired, Length,
                                NumberRange, Optional, Regexp, ValidationError)

# product categories (must match the CHECK constraint in database/create_tables.sql)
CATEGORIES = [('Face', 'Face'), ('Eyes', 'Eyes'), ('Lips', 'Lips'),
              ('Cheeks', 'Cheeks'), ('Brows', 'Brows')]


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


# create a class for the web elements needed to add a product to the vault
class ProductForm(FlaskForm):
    barcode = StringField('Barcode (EAN/UPC)', validators=[
        Optional(), Regexp(r'^[0-9]{8,13}$', message='Barcode must be 8 to 13 digits.')])
    brand = StringField('Brand', validators=[DataRequired(), Length(max=60)])
    product_name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    shade = StringField('Shade', validators=[Optional(), Length(max=50)])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    opened_date = DateField('Opened Date', validators=[DataRequired()])
    pao_months = IntegerField('PAO (months)', validators=[
        InputRequired(), NumberRange(min=1, max=60, message='PAO must be 1 to 60 months.')])
    pan_progress = IntegerField('Pan Progress (%)', default=0, validators=[
        InputRequired(), NumberRange(min=0, max=100, message='Pan progress must be 0 to 100.')])
    submit = SubmitField('Add to Vault')

    # extra check: a product cannot be opened in the future
    def validate_opened_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError('Opened date cannot be in the future.')
