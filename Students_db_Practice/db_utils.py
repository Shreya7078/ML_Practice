import sqlite3

DB_NAME = 'students.db'

# Helper function to get a connection
def get_connection():
    return sqlite3.connect(DB_NAME)


def reset_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Delete all rows from students
    cursor.execute("DELETE FROM students")

    conn.commit()
    conn.close()
    print("Database reset successfully")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            subject TEXT,
            roll_no INTEGER,
            marks INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_student(name, subject, roll_no, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, subject, roll_no, marks)
        VALUES (?, ?, ?, ?)
    ''', (name, subject, roll_no, marks))
    conn.commit()
    conn.close()

def fetch_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def update_student(id, name, subject, roll_no, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students
        SET name=?, subject=?, roll_no=?, marks=?
        WHERE id=?
    ''', (name, subject, roll_no, marks, id))
    conn.commit()
    conn.close()

def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM students
        WHERE id=?
    ''', (id,))
    conn.commit()
    conn.close()

def find_average_marks(subject):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    # case-insensitive comparison + strip spaces
    cursor.execute("""
        SELECT AVG(marks)
        FROM students
        WHERE LOWER(TRIM(subject)) = LOWER(TRIM(?))
    """, (subject,))
    result = cursor.fetchone()
    conn.close()
    return float(result[0]) if result and result[0] is not None else None


def find_topper():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, subject, marks
        FROM students
        ORDER BY marks DESC
        LIMIT 1
    ''')
    topper = cursor.fetchone()
    conn.close()
    if topper:
        return {"name": topper[0], "subject": topper[1], "marks": topper[2]}
    return None


reset_database()
create_table()
insert_student('Alice', 'Maths', 1, 85)
insert_student('Bob', 'Science', 2, 90)
insert_student('Charlie', 'Maths', 3, 95)


