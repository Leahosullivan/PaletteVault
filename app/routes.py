# import the Flask functions used by the routes
from flask import render_template, redirect, url_for, request, flash
# import app variable from app package
from app import app
# import the form classes from our forms.py file
from app.forms import LoginForm, RegistrationForm, ProductForm
# import the product database functions
from app.products import get_vault, find_by_barcode, add_product


# create an association for the URL /
@app.route('/')
# create an association for the URL /index
@app.route('/index')
# create the index page to display the vault collection from the database
def index():
    products = get_vault(app.config['DEMO_USER_ID'])

    # dashboard figures calculated from the database rows
    expiring = [p for p in products if p['status'] != 'Fresh']
    avg_pan = round(sum(p['pan_progress'] for p in products) / len(products)) if products else 0

    return render_template('index.html', title='Home', products=products,
                           expiring_count=len(expiring), avg_pan=avg_pan)


# create an association for the URL /products/add
@app.route('/products/add', methods=['GET', 'POST'])
# Use Case 1: scan or type a barcode, look it up, then save the product
def add():
    form = ProductForm()
    lookup = None

    # GET /products/add?barcode=... comes from the scan bar on the Home page
    barcode = request.args.get('barcode', '').strip()
    if request.method == 'GET' and barcode:
        form.barcode.data = barcode
        lookup = find_by_barcode(barcode)
        if lookup:
            form.brand.data = lookup['brand']
            form.product_name.data = lookup['product_name']
            form.shade.data = lookup['shade']
            form.category.data = lookup['category']
            form.pao_months.data = lookup['pao_months']
        else:
            # alternative flow: barcode not found, user enters details manually
            flash('Barcode not found in PaletteVault - please enter the details manually.',
                  'info')

    if form.validate_on_submit():
        add_product(app.config['DEMO_USER_ID'], {
            'barcode': form.barcode.data,
            'brand': form.brand.data.strip(),
            'product_name': form.product_name.data.strip(),
            'shade': form.shade.data.strip() if form.shade.data else '',
            'category': form.category.data,
            'opened_date': form.opened_date.data,
            'pao_months': form.pao_months.data,
            'pan_progress': form.pan_progress.data,
        })
        flash(f'{form.product_name.data} was added to your vault.', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html', title='Add Product', form=form, lookup=lookup)


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
