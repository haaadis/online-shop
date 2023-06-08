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
	return render_template('home.html',orders=orders)
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
			session['admin']=True
			session['loggedin'] = True
			session['id'] = 0
			session['username'] = list(admin.keys())[0]
			return render_template('home.html',message=message)
		elif email not in admin:
			conn = sqlite3.connect('users.db')
			cursor = conn.cursor()
			cursor.execute('SELECT * FROM users WHERE email = ? AND password =?',(email, password,))
			user = cursor.fetchone()
			if user:
			        session['admin']=False
				session['loggedin'] = True
				session['id'] = user[0]
				session['username'] = user[1]
				message = 'Logged in successfully'
				conn.close()
				return render_template('home.html',message=message)
			else:
				message = 'please register first'
		else:
			message = 'Please enter correct email / password !'
	return render_template('login.html',message=message)

# Make function for logout session
@app.route('/logout')
def logout():
	session.pop('admin', None)
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

			   
def check_quantity(quantity,stock): 
            if stock=='UNAVAILABLE':
                return False
            elif (quantity > int(stock)) :
                return False
            else:
                 return True			   
			   
@app.route('/cart')
def cart():
    total_price=sum([x[3]*x[2] for x in orders])
    tax =sum([x[3]*x[2] for x in orders])*0.09 
    return render_template('shoppingcart.html', orders=orders,tax=tax,total_price=total_price,total=tax+total_price,enumerate=enumerate)

@app.route('/add<m>', methods=['POST'])
def add(m):
	conn = sqlite3.connect('products.db')
	cursor = conn.cursor()
	stock=cursor.execute("SELECT stock FROM products WHERE name=?", (m,)).fetchone()
	if request.method == 'POST' and 'color' in request.form  and 'size' in request.form:
		quantity = int(request.form.get('quantity'))
		description = request.form.get('color') +','+ request.form.get('size')
		price = cursor.execute("SELECT price FROM products WHERE name=?", (m,)).fetchone()
		if check_quantity(quantity,stock):
			orders.append([m,description,quantity,price])
			message = m+'added to cart'
		else:
			message='not available in that quantity' 
	else:
		message = 'choose some variants'
	return redirect(url_for('details',m=m,message=message))
    
@app.route('/delete/<int:index>')
def delete(index):
    orders.pop(index)
    return redirect(url_for('cart'))

@app.route('/empty')
def empty_cart():
	orders.clear()
	return redirect(url_for('home'))
			   
@app.route('/update_qnt/<int:index>')
def update_qnt(index):
    quantity = request.form.get('quantity')
    orders[index][2]=quantity
    return redirect(url_for('cart'))
			  
#get information of user after shoppingcart
@app.route('/info')
def info():
	firstname = request.form['firstname']
	lastname = request.form['lastname']
	phone = request.form['phone']
	address = request.form['address']
	zipcode = request.form['zipcode']
	conn=sqlite3.connect('.db')
	c=conn.cursor()
	c.execute("SELECT DISTINCT country FROM  ")
	country = c.fetchall()
	selected_country=request.form.get["country"]
	c.execute("SELECT DISTINCT FROM  WHERE country=?",(selected_country,))
	states=c.fetchall()
	selected_state=request.form.get["state"]
	c.execute("SELECT FROM cities WHERE state=?",(selected_state,))
	cities=c.fetchall()
	return render_template('info.html',country=country,states=states,cities=cities)

#function to update stocks after payment
def update_stocks(x):
	try:
		conn = sqlite3.connect('products.db')
		cursor = conn.cursor()
		y=cursor.execute("SELECT stock FROM products WHERE name=?", (x[0],)).fetchone() - x[2]
		cursor.execute("UPDATE products SET stock=? WHERE name = ?",(y,x[0],))
		cursor.execute("UPDATE products SET stock=? WHERE stock = ?",('UNAVAILABLE',0,))
		conn.commit()
	finally:
		conn.close()

@app.route('/checkout')
def checkout():
	if len(request.form['cardnumber'])==16:
		message='your orders'
		for i in orders:
			update_stocks(i)
		return redirect('home',message=message)
	elif len(request.form['cardnumber'])!=16:
		message='Invalid card.no'
		return render_template('checkout.html',message=message)
	return render_template('checkout.html')
			   
			   
			   
class UploadFileForm(FlaskForm):
    file = FileField('File', validators= [InputRequired()])
    submit = SubmitField('Upload File')

@app.route('/add_product')
def add_product():
    form = UploadFileForm()
    if form.validate_on_submit() and request.method == 'POST' and 'name' in request.form and 'size' in request.form and 'color' in request.form and 'price' in request.form and 'stock' in request.form:
        name = request.form['productName']
        code=str(random.randint(10000,100000))+chr(random.randint(ord('a'), ord('z')))
        stock =  request.form['stock']
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD-FOLDER'],secure_filename(file.filename)))
        image_address = 'static/images/image_products/'+str(file.filename)
        size = str(request.form['productsize'])
        color = str(request.form['productcolor'])
        price = request.form['price']
        category = request.form['category']
        discount = request.form['discount']
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        params = (name,code,image_address,stock, size, color,price,category,discount)
        cursor.execute("INSERT INTO products VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
        conn.commit()
        conn.close()
        message = 'File has been uploaded.'
    else:
        message = "You need to fill the form!"
    return render_template('add_item.html', message=message, form=form)

@app.route('/delete_product')
def delete_product(x):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE name=? AND code=?",(x[1],x[2],))
    conn.commit()
    conn.close()
    return redirect('products',x=x[7])
