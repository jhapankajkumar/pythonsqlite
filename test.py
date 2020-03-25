import  sqlite3


# start connection
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create table
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)


# insert singale
user = (1, 'pankaj', 'asdf')
add_user = "INSERT INTO users VALUES (?,?,?)"

cursor.execute(add_user, user)


users = [
    (2, 'jyoti', '1234'),
    (3, 'gulugulu', '4534')
]

# insert mutliple
cursor.executemany(add_user, users)

# retrieve data

get_data = "SELECT * from users"

rows = cursor.execute(get_data)
for (_id, username, password) in rows:
    print("ID:", _id)
    print("Username:", username)
    print("password:", password)


connection.commit()
connection.close()
