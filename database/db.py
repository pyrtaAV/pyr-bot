import sqlite3 as db

conn = db.connect('users_pyr.db')
cursor = conn.cursor()


def sql_start():
    if conn:
        print('Data base connected OK!')
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       email TEXT,
                       password INTEGER,
                       payed BOOLEAN)
                   """)
    conn.commit()


async def add_to_db(user_data):
    cursor.execute("INSERT INTO users (email, password, payed) VALUES (?, ?, ?)",
                   (user_data['email'],
                    user_data['password'],
                    True)
                   )
    conn.commit()


async def get_all_from_db():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


async def get_one_from_db(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


async def delete_from_db(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()


def sql_stop():
    conn.close()
    print('Connection close!')
