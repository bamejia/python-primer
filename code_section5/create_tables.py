import _sqlite3


connection = _sqlite3.connect("data.db")
cursor = connection.cursor()

create_table = "CREATE TABLE if not exists USERS (id INTEGER primary key, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE if not exists ITEMS (id INTEGER primary key, name text, price real)"
cursor.execute(create_table)

# insert_query = "INSERT INTO items VALUES (NULL, ?, ?)"
# items = {
#     ("water", 1.99),
#     ("gatorade", 2.50)
# }
# cursor.executemany(insert_query, items)

connection.commit()
connection.close()