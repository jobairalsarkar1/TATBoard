from app import app
from flask import render_template
from .models import User, Customer


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)


@app.route('/add_customers')
def add_customer():
    return render_template('add_customers.html')
