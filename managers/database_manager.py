import sqlite3

class UserDatabase:

    def __init__(self, db_path='./data/users.db'):
        """Initialize the UserDatabase class with the path to the SQLite database.

        Args:
            db_path (str, optional): Path to the SQLite database file. Defaults to './data/users.db'.
        """
        self.db_path = db_path

    def _connect(self):
        """Create a connection to the SQLite database.

        Returns:
            sqlite3.Connection : A connection to the SQLite database.
        """
        return sqlite3.connect(self.db_path)



    def _initialize_database(self):
        
        """Initialize the database by creating the users table and setting up a default admin user. With admin as a username and adminpassword as a password """
        
        conn = self._connect()
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

        # Create a persistent admin user
        admin_password = bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            'INSERT OR IGNORE INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
            ('admin', admin_password, 'jafjafnora@gmail.com', 1)
        )

        conn.commit()
        conn.close()
        print("done")
        
        
    def add_user(self, username, hashed_password, email, is_admin):  
        """Add a new user to the database.

        Args:
            username (str): The username of the user.
            password (str): The plain-text password of the user.
            email (str): The email of the user.
            is_admin (int): Whether the user is an admin (1) or not (0). Defaults to 0.

        Returns:
            bool: True if the user is successfully added, False otherwise.===> to be changed ! METTRE DANS UN TRY EXCEPT FINNALY 
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
            (username, hashed_password, email, is_admin)
        )
        conn.commit()
        conn.close()

    def get_user(self, username):
        """Retrieve a user's information by username.
        
        Args:
            username (str) : The username of the user to retrieve.

        Returns:
            tuple : A tuple containing all the user's information, or None otherwise. 
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_users(self):
        """Retrieve all users in the database.

        Returns:
            list : A list of tuples containing users informations.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, is_admin FROM users')
        users = cursor.fetchall()
        conn.close()
        return users

    def delete_user(self, user_id):
        """ Delete a user by their ID.
        
        Args:
            user_id (int): The ID of the user to delete.

        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

    def get_user_infos(self, username):
        """Retrieve specific information about a user by username.

        Args : 
            username (str): The username of the user.
            
        Returns:
            tuple : A tuple containing the user's ID, username, email, and is_admin status.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, is_admin FROM users WHERE username = ?', (username,))
        infos = cursor.fetchone()
        conn.close()
        return infos
