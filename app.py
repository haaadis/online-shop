# Import all important libraries
from flask import Flask, redirect, url_for, request, render_template ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import sqlite3
import random
import json
import requests
app = Flask(__name__)
app.secret_key = "secret key" 

admin = {'kunal@gmail.com': '1234'}   #admin email and password
orders=[]
@app.route('/')
def home():
	return render_template('home.html')
@app.route('/<m>')
def details(m):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    
    price=c.execute("SELECT price  FROM products WHERE name=?", (m,)).fetchone()
    color=c.execute("SELECT color  FROM products WHERE name=?", (m,)).fetchone()
    name=c.execute("SELECT name  FROM products WHERE name=?", (m,)).fetchone()
    size=c.execute("SELECT size  FROM products WHERE name=?", (m,)).fetchone()
    category=c.execute("SELECT category  FROM products WHERE name=?", (m,)).fetchone()
    tomans=price[0]
    url = f'https://api.exchangerate-api.com/v4/latest/IRR'
    response = requests.get(url)
    data = response.json()
    dollars = float(price[0])*data['rates']['USD']
    result = {'dollars': dollars}



    

    return render_template('details.html', m=m ,enumerate=enumerate, p

@app.route('/login', methods=['GET', 'POST'])
def login():
	message = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		if email in admin and admin[email] == password:
			message = 'Logged in successfully'
			return render_template('home.html',message=message,adminlog=True,log=True)
		elif email not in admin:
			conn = sqlite3.connect('users.db')
			cursor = conn.cursor()
			cursor.execute('SELECT * FROM users WHERE email = ? AND password =?',(email, password,))
			user = cursor.fetchone()
			if user:
				session['loggedin'] = True
				session['id'] = user[0]
				session['username'] = user[1]
				message = 'Logged in successfully'
				conn.close()
				return render_template('home.html',message=message,adminlog=False,log=True)
			else:
				message = 'please register first'
		else:
			message = 'Please enter correct email / password !'
	return render_template('login.html',message=message)

# Make function for logout session
@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('userid', None)
	session.pop('email', None)
	return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	message = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		conn = sqlite3.connect('users.db')
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM users WHERE email=?',(email))
		account = cursor.fetchone()
		if account:
			message = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			message = 'Invalid email address !'
		elif not username or not password or not email:
			message = 'Please fill out the form !'
		else:
			params = (username, email, password )
			cursor.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", params)
			conn.commit()
			conn.close()
			message = 'You have successfully registered !'
	elif request.method == 'POST':
		message = 'Please fill out the form !'
	return render_template('register.html', message=message)


app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
	message = ''
	if request.method == 'POST' and 'Email' in request.form  and 'new Password' in request.form:
		newpassword = request.form['new Password']
		email = request.form['Email']
		conn = sqlite3.connect('users.db')
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM users WHERE email =?',(email))
		account = cursor.fetchone()
		if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			message = 'Invalid email address !'
		elif account==False:
			message = "Account doesn't exist !"
		else:
			cursor.execute('UPDATE users SET password = ?  WHERE email =? ',(newpassword,email,))
			conn.commit()
			conn.close()
			message = "You're password has successfully changed !"
			return render_template('login.html',message=message)
            
	elif request.method == 'POST':
		message = 'Please fill out the form !'			
	return render_template('resetpassword.html', message=message)
			   
@app.route('/cart')
def cart():
    total_price=sum([x[3]*x[2] for x in orders])
    tax =sum([x[3]*x[2] for x in orders])*0.09 
    return render_template('shoppingcart.html', orders=orders,tax=tax,total_price=total_price,total=tax+total_price,enumerate=enumerate)

@app.route('/add<m>', methods=['POST'])
def add(m):
    description = request.form.get('color') +','+ request.form.get('size')
    quantity = int(request.form.get('quantity'))
    price = 1000
    orders.append([m,description,quantity,price])
    message = m+'added to cart' 
    return redirect(url_for('details',m=m,message=message))
    
@app.route('/delete/<int:index>')
def delete(index):
    orders.pop(index)
    return redirect(url_for('cart'))

@app.route('/empty')
def empty_cart():
	orders.clear()
	return redirect(url_for('home'))
