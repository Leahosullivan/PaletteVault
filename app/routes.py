# import the Flask functions used by the routes
from flask import render_template, redirect, url_for, flash, abort
# import app variable from app package
from app import app
# import the form classes from our forms.py file
from app.forms import LoginForm, RegistrationForm, UsageForm
# import the usage logging database functions
from app.usage import get_products_with_usage, get_product, get_usage_history, log_usage


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


# create an association for the URL /usage
@app.route('/usage')
# list the user's products so one can be picked for logging
def usage():
    products = get_products_with_usage(app.config['DEMO_USER_ID'])
    return render_template('usage.html', title='Usage Log', products=products)


# create an association for the URL /usage/<product_id>
@app.route('/usage/<int:product_id>', methods=['GET', 'POST'])
# Use Case 3: log new pan progress for one product and show its history
def log_product_usage(product_id):
    product = get_product(product_id, app.config['DEMO_USER_ID'])
    if product is None:
        abort(404)

    form = UsageForm()

    if form.validate_on_submit():
        log_usage(product_id, form.pan_progress.data, form.notes.data)
        flash(f"Usage saved - {product['product_name']} is now at "
              f"{form.pan_progress.data}% pan progress.", 'success')
        return redirect(url_for('log_product_usage', product_id=product_id))

    # pre-fill the box with the current value the first time the page loads
    if form.pan_progress.data is None and not form.is_submitted():
        form.pan_progress.data = product['pan_progress']

    history = get_usage_history(product_id)
    return render_template('log_usage.html', title='Log Usage', product=product,
                           form=form, history=history)


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
