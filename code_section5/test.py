import _sqlite3
import sys


connection = _sqlite3.connect("data.db")
cursor = connection.cursor()

select_query = "SELECT * FROM users"
rows = cursor.execute(select_query)
print([row for row in rows])
connection.close()
sys.exit()

create_table = "CREATE TABLE USERS (id int, username text, password text)"

cursor.execute(create_table)

user = (1, "jose", "asdf")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = {
    (2, "rolf", "asdf2"),
    (3, "jerry", "pass")
}
cursor.executemany(insert_query, users)

connection.commit()
connection.close()