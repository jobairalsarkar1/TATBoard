from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def landing():
    return render_template('landing.html')


@app.route("/customers")
def customers():
    return render_template('customers.html')


@app.route("/add_customer")
def add_customer():
    return render_template('add_customers.html')


if __name__ == '__main__':
    app.run(debug=True)
