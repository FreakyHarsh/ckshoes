import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12388883'
app.config['MYSQL_PASSWORD'] = '4p7rqEczmi'
app.config['MYSQL_DB'] = 'sql12388883'

mysql = MySQL(app)


@app.route('/')
def login():
    # TODO: Add login logic
    return render_template('login.html')

# TODO: Remove get later

# TODO: remove get


@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.values.get('username')
    password = request.values.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stocks")
    data = cur.fetchall()
    # data = tuple(reversed(data))
    length = len(data)
    cur.close()
    if (username == 'admin' and password == 'admin@123'):
        return render_template('dashboard.html', data=data, length=length)
    else:
        return render_template('404.html', title='Invalid Password', message="Username or password is invalid")


@app.route('/add-stock', methods=['POST'])
def addstock():
    details = request.form
    ename = details['employee-name']
    orderno = details['order-no']
    brand = details['brand']
    no_of_shoes = details['no-of-shoes']
    size = details['size']
    price = details['price']
    arrived_on = details['arrived-on']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO stocks(employee_name,order_no, brand, no_of_shoes, size, price, arrived_on) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ename, orderno, brand, no_of_shoes, size, price, arrived_on))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('dashboard', username='admin', password='admin@123'), code=307)
    # return render_template('dashboard.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', title='404', message='something went wrong')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 4444)), host='0.0.0.0')
