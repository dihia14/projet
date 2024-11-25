
import sqlite3


def add_user_database (username, hashed_password, email, is_admin): 
    conn = sqlite3.connect('./data/users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
                (username, hashed_password, email, is_admin))
    conn.commit()
    conn.close()
    
    
def get_user(username):
    conn = sqlite3.connect('./data/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user




def get_users_db():
    conn = sqlite3.connect('./data/users.db')

    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, is_admin  FROM users')
    users = cursor.fetchall()
    conn.close()
    return users
    #return [dict(user) for user in users]  


def delete_user_database(user_id) : 
    #print("USERERRRRR", user_id)
    user_id = int(user_id)  

    conn = sqlite3.connect('./data/users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    
    
def get_user_infos(username): 
    conn = sqlite3.connect('./data/users.db')
    cursor = conn.cursor()
    #cursor.execute('SELECT id, username, email, is_admin  FROM users')
    #cursor.execute('SELECT id, username, email  FROM users WHERE id = ?', (user_id))  #password ? 
    cursor.execute('SELECT id, username, email, is_admin FROM users WHERE username = ?', (username,))
    infos = cursor.fetchone()
    conn.close()
    return infos
