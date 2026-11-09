# import render_template, redirect and url_for functions from flask
from flask import render_template, redirect, url_for
# import app variable from app package
from app import app
# import LoginForm and RegistrationForm classes from our forms.py file
from app.forms import LoginForm, RegistrationForm


# create an association for the URL /
@app.route('/')
# create an association for the URL /index
@app.route('/index')
# create the index page to display the vault collection
def index():
    # create a list of dictionaries to hold product information
    products = [
        {
            'brand': 'NARS Cosmetics',
            'name': 'Radiant Creamy Concealer',
            'shade': 'Custard',
            'category': 'Face',
            'pan': 65,
            'status': '7 Days Left',
            'expiring': True
        },
        {
            'brand': 'Fenty Beauty',
            'name': 'Gloss Bomb Universal Luminiser',
            'shade': 'Fenty Glow',
            'category': 'Lips',
            'pan': 20,
            'status': 'Fresh',
            'expiring': False
        }
    ]

    return render_template('index.html', title='Home', products=products)


# create an association for the URL /about
@app.route('/about')
# create the about page
def about():
    return render_template('about.html', title='About Us')


# create an association for the URL /login (GET to show the form, POST to submit it)
@app.route('/login', methods=['GET', 'POST'])
# create the login page to display web form for user
def login():
    # create an instance of a LoginForm obj and store in a variable called form
    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


# create an association for the URL /register
@app.route('/register', methods=['GET', 'POST'])
# create the register page to display web form for new user
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
