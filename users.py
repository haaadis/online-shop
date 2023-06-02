import sqlite3
conn = sqlite3.connect('users.db')
cursor=conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  	username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
  	email varchar(100) NOT NULL
) ''')

conn.commit()
conn.close()
