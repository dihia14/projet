import sqlite3
import bcrypt

# connexion a à db 
conn = sqlite3.connect('../data/users.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE,              
    is_admin INTEGER DEFAULT 0       
)
''')

mail = 'jafjafnora@gmail.com'

# persistent user (admin)
admin_password = bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt())
cursor.execute('INSERT OR IGNORE INTO users (username, password, email,  is_admin) VALUES (?, ?,?, ?)', 
               ('admin', admin_password, mail,  1))


# save and close the connection 
conn.commit()
conn.close()

print("done")
