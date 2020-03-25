import sqlite3

connection  = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

cursor.execute(create_user_table)

connection.commit()
connection.close()