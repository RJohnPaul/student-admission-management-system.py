import sqlite3
import random
from datetime import datetime

class AdmissionSystem:
    def __init__(self, db_name='admission_system.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                gender TEXT,
                admission_date TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Enrollments (
                enrollment_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date TEXT,
                FOREIGN KEY(student_id) REFERENCES Students(student_id),
                FOREIGN KEY(course_id) REFERENCES Courses(course_id)
            )
        ''')
        self.conn.commit()

    def add_student(self, first_name, last_name, age, gender):
        admission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO Students (first_name, last_name, age, gender, admission_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, age, gender, admission_date))
        self.conn.commit()

    def add_course(self, course_name):
        self.cursor.execute('''
            INSERT INTO Courses (course_name)
            VALUES (?)
        ''', (course_name,))
        self.conn.commit()

    def enroll_student(self, student_id, course_id):
        enrollment_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO Enrollments (student_id, course_id, enrollment_date)
            VALUES (?, ?, ?)
        ''', (student_id, course_id, enrollment_date))
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute('SELECT * FROM Students')
        return self.cursor.fetchall()

    def get_all_courses(self):
        self.cursor.execute('SELECT * FROM Courses')
        return self.cursor.fetchall()

    def get_student_enrollments(self, student_id):
        self.cursor.execute('''
            SELECT Courses.course_name, Enrollments.enrollment_date
            FROM Courses
            JOIN Enrollments ON Courses.course_id = Enrollments.course_id
            WHERE Enrollments.student_id = ?
        ''', (student_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

# Example Usage
admission_system = AdmissionSystem()

# Add students and courses
admission_system.add_student("John", "Doe", 20, "Male")
admission_system.add_student("Jane", "Smith", 22, "Female")
admission_system.add_course("Computer Science")
admission_system.add_course("Mathematics")

# Enroll students in courses
admission_system.enroll_student(1, 1)  # John enrolled in Computer Science
admission_system.enroll_student(2, 2)  # Jane enrolled in Mathematics

# Get information
print("All Students:")
print(admission_system.get_all_students())

print("\nAll Courses:")
print(admission_system.get_all_courses())

print("\nJohn's Enrollments:")
print(admission_system.get_student_enrollments(1))

# Close the database connection
admission_system.close_connection()
