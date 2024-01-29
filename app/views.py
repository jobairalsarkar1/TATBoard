from app import app
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/customers')
def customers():
    return render_template('customers.html')


@app.route('/add_customers')
def add_customer():
    return render_template('add_customers.html')
