import sqlite3
from werkzeug.security import generate_password_hash
from backend.models import create_all_tables

DATABASE = 'placement_portal.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn):
    if conn:
        conn.close()

def init_db():
    create_all_tables()
    create_admin()
    print("DONE DATABASE INITIALIZATION")

def create_admin():
    conn = get_db()
    cursor = conn.cursor()
    hashed_password = generate_password_hash('admin123')
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', 
        ('admin1',
        'admin@ppa.com',
        hashed_password, 
        'admin'
        ))
        conn.commit()
        print("ADMIN USER CREATED")
    except sqlite3.Error as e:
        print(f"Error creating admin user: {e}")
    finally:
        close_db(conn)

