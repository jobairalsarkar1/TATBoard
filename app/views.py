from app import app, db
from flask import render_template, request, redirect, url_for, session, flash, abort
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


@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if 'logged_in' not in session:
        flash('You must be logged in')
        return redirect(url_for('home'))
    valid = session['logged_in']
    logged_user = User.query.get(session['user_id'])
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        customers = Customer.query.filter(
            (Customer.name.ilike(f'%{search_query}%')) |
            (Customer.email.ilike(f'%{search_query}%')) |
            (Customer.phone.ilike(f'%{search_query}%')) |
            (Customer.address.ilike(f'%{search_query}%'))
        ).all()
        print(customers)
        return render_template('customers.html', customers=customers, user=logged_user, valid=valid)
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
        # print(address)
        amount = request.form.get('total')
        user_id = session['user_id']
        new_customer = Customer(name=name, phone=phone,
                                address=address, amount=amount, user_id=user_id)
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer Information added successfully.')
    valid = session['logged_in']
    logged_user = User.query.get(session['user_id'])
    return render_template('add_customers.html', valid=valid, user=logged_user)


@app.route('/customers/<int:customer_id>', methods=['GET', 'POST'])
def customer_detail(customer_id):
    if 'logged_in' not in session:
        flash('You must be Logged in.')
        return redirect(url_for('home'))
    customer = Customer.query.get_or_404(customer_id)
    valid = session['logged_in']
    logged_user = User.query.get(session['user_id'])
    return render_template('customer_detail.html', customer=customer, valid=valid, user=logged_user)


# @app.route('/customer/<int:customer_id>/delete', methods=['POST'])
# def delete_customer(customer_id):
#     if 'logged_in' not in session:
#         flash('You must be logged in')
#         return redirect(url_for('home'))

#     if not session.get('is_admin'):
#         abort(403)  # Forbidden

#     customer = Customer.query.get_or_404(customer_id)
#     db.session.delete(customer)
#     db.session.commit()
#     flash('Customer deleted successfully.')
#     return redirect(url_for('customers'))
