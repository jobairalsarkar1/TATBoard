from app import app, db
from flask import render_template, request, redirect, url_for, session, flash
from .models import User, Customer


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        form_user = User.query.filter_by(email=email).first()
        if form_user and form_user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = form_user.id
            return redirect(url_for('customers'))
        else:
            return 'Invalid Email or Password.'
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/customers')
def customers():
    if 'logged_in' not in session:
        flash('You must be logged in')
        return redirect(url_for('home'))
    valid = session['logged_in']
    logged_user = User.query.get(session['user_id'])
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers, user=logged_user, valid=valid)


@app.route('/add_customers', methods=['GET', 'POST'])
def add_customer():
    if 'logged_in' not in session:
        flash('You must be logged in')
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('first-name')
        phone = request.form.get('phone')
        address = request.form.get('delivery-address')
        print(address)
        amount = request.form.get('total')
        user_id = session['user_id']
        new_customer = Customer(name=name, phone=phone,
                                address=address, amount=amount, user_id=user_id)
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer Information added successfully.')
    valid = session['logged_in']
    return render_template('add_customers.html', valid=valid)
