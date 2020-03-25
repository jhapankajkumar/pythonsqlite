import sqlite3

connection  = sqlite3.connect('data.db')
cursor = connection.cursor()

create_item_table = "CREATE TABLE IF NOT EXISTS items (name text, price text)"
cursor.execute(create_item_table)

connection.commit()
connection.close()