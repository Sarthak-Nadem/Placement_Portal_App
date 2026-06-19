#===============================================
'''users
students
companies
placement_drives
applications
placements          ← dashboard statistics
notifications       ← email & alerts'''
#===============================================

import sqlite3

DATABASE = 'placement_portal.db'

def create_users_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT  NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL Check(role IN ('admin','company','student')),
                active INTEGER NOT NULL DEFAULT 0,
                verification_token TEXT,    
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def create_students_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                branch TEXT Check(branch IN ('CSE', 'ECE', 'ME', 'CE', 'EE', 'IT')),
                graduation_year INTEGER,
                cgpa REAL,
                phone TEXT,
                resume_path TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()


def create_companies_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                company_name TEXT NOT NULL,

                hr_name TEXT NOT NULL,
                hr_email TEXT,
                website TEXT,
                description TEXT,
                approval_status TEXT NOT NULL DEFAULT 'pending' CHECK(approval_status IN ('pending', 'approved', 'rejected')),
                active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

def create_placement_drive_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS placement_drives (
                drive_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,

                job_title TEXT NOT NULL,
                job_description TEXT,

                branch_eligibility TEXT,
                min_cgpa REAL,
                graduation_year INTEGER,

                application_deadline TIMESTAMP,
                status TEXT NOT NULL DEFAULT 'upcoming' CHECK(status IN ('upcoming', 'ongoing', 'completed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            )
        ''')
        conn.commit()

def create_applications_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                drive_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'applied' CHECK(status IN ('applied', 'shortlisted', 'rejected', 'accepted')),
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                interview_date TIMESTAMP,
                remarks TEXT,

                FOREIGN KEY (drive_id) REFERENCES placement_drives(drive_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')
        conn.commit()

#==================================================================================
def create_notifications_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()


def create_placement_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS  placements (
                placement_id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,

                salary_package REAL,
                joining_date DATE,

                FOREIGN KEY(student_id) REFERENCES students(student_id),

                FOREIGN KEY(company_id) REFERENCES companies(company_id)
            )
        ''')
        conn.commit()



#=========================================
def create_all_tables():
    create_users_table()
    create_students_table()
    create_companies_table()
    create_placement_drive_table()
    create_applications_table()
    create_notifications_table()
    create_placement_table()
#=========================================

