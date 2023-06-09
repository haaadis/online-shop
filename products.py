import sqlite3



conn = sqlite3.connect('products.db')
c=conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name varchar(255)  NOT NULL,
	code varchar(255)  NOT NULL,
    image_address varchar(255)  NOT NULL,
    size text ,
    color text ,
	price INTEGER  NOT NULL,
    category text NOT NULL,
    stock varchar(255) NOT NULL,
    discount INTEGER  NOT NULL,
    new_price INTEGER  NOT NULL
    
    );''')


params = ('bag1','12341H','https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-neverfull-mm-monogram-handbags--M40995_PM2_Front%20view.jpg', 'M', 'RED',345000,'bags',5,10,5)
params2= ('bag2','13341H', 'https://us.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-neverfull-mm-monogram-handbags--M40995_PM2_Front%20view.jpg','M', 'yeloow',589000,'bags',9,20,4)
c.execute("INSERT INTO products VALUES (NULL,?,?, ?, ?, ?, ?, ?, ?,?,?)", params)
c.execute("INSERT INTO products VALUES (NULL,?,?, ?, ?, ?, ?, ?, ?,?,?)", params2)


conn.commit()
print(c.fetchall())
conn.close()
