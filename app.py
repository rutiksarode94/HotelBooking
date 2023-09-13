import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    adhar = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    room = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, adhar, address, room, gender, age, city):
        self.name = name
        self.email = email
        self.adhar = adhar
        self.address = address
        self.room = room
        self.gender = gender
        self.age = age
        self.city = city


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/booknow', methods=['GET', 'POST'])
def booknow():
    success_message = None
    back_url = url_for('home')

    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data and perform booking as required
        name = request.form['name']
        email = request.form['email']
        adhar = request.form['adhar']
        address = request.form['address']
        room = request.form['room']
        gender = request.form['gender']
        age = request.form['age']
        city = request.form['city']

        # Create a new Customer object and add it to the database
        new_customer = Customer(name=name, email=email, adhar=adhar, address=address, room=room, gender=gender, age=age, city=city)
        db.session.add(new_customer)
        db.session.commit()

        # Set the success message to be displayed in the template
        success_message = "Booking successful! Thank you for choosing our hotel."

    return render_template('booknow.html', success_message=success_message, back_url=back_url)


@app.route('/viewbooking')
def viewbooking():
    if 'username' not in session:

        return redirect(url_for('login'))

    customers = Customer.query.all()

    back_url = request.referrer

    return render_template('viewbooking.html', customers=customers, back_url=back_url)


@app.route('/customers/<int:id>/edit', methods=['GET', 'POST'])
def edit_customer(id):
    if 'username' not in session:

        return redirect(url_for('login'))

    # Retrieve the customer record with the given id from the database
    customer = Customer.query.get_or_404(id)

    if request.method == 'POST':
        # Update customer data with the values from the form
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.adhar = request.form['adhar']
        customer.address = request.form['address']
        customer.room = request.form['room']
        customer.gender = request.form['gender']
        customer.age = request.form['age']
        customer.city = request.form['city']

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the viewbooking page after successful edit
        return redirect(url_for('viewbooking'))

    return render_template('edit_customer.html', customer=customer)


users = {
    "john_doe": {"password": "12345"},
    "jane_smith": {"password": "54321"},
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            # Login successful, store the username in the session
            session['username'] = username
            flash("Login successful. Welcome, {}!".format(username))
            return redirect(url_for('home'))
        else:
            # Display an error message if login fails
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')


users = {
    "john_doe": {"password": "12345"},
    "jane_smith": {"password": "54321"},
}


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if username in users:
            error_message = "Username already taken. Please choose another username."
            return render_template('signup.html', error_message=error_message)

        users[username] = {"password": password}

        # Registration successful, display a success message
        flash("Account created successfully. You can now log in with your credentials.")

        # Redirect to the login page
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    # Clear the user's session data (log out)
    session.clear()
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Here, you can add code to process the form data or save it to a database
    return render_template('thankyou.html', name=name)


@app.route('/customers/<int:id>/delete', methods=['GET', 'POST'])
def delete_customer(id):
    if 'username' not in session:

        return redirect(url_for('login'))

    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('viewbooking'))
    return render_template('delete.html', customer=customer)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
