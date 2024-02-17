from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'\x0e!uAz\xed\xd2\xadeu\xb0\xa3\xae\xd0\\\xce\xb40\x7f\xd4)\xdb\\\r'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ABc()!?12=%'
app.config['MYSQL_DB'] = 'project1'

mysql = MySQL(app)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phonenumber = request.form['phonenumber']

        # Hash the password before storing in the database
        hashed_password = generate_password_hash(password)

        # Insert user data into MySQL
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO eeetable VALUES (%s, %s, %s)", (username, hashed_password, phonenumber))
        mysql.connection.commit()
        cur.close()

        # Redirect to the login route (update the route if needed)
        return redirect(url_for('login'))

    return render_template('register1.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM eeetable WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            # Set user session
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))

    return render_template('login.html')

# Dashboard route (example)
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        # Retrieve user information from the database
        username = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM eeetable WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Pass user information to the template
            return render_template('dashboard.html', user=user)
        else:
            # Handle the case where user information is not found
            return render_template('dashboard.html', user=None)
    else:
        return redirect(url_for('login'))

'''
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' in session:
        return render_template('html_code.html')
    else:
        return redirect(url_for('login'))
    '''

# Logout route
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
