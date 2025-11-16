#!/usr/bin/env python3
import psycopg2
from config.settings import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD

def view_data():
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        cursor = conn.cursor()
        
        # Show Supervisors
        print("👨‍💼 SUPERVISORS")
        print("=" * 50)
        cursor.execute("SELECT * FROM supervisors ORDER BY created_at DESC")
        supervisors = cursor.fetchall()
        for row in supervisors:
            print(f"ID: {row[0]} | Username: {row[1]} | Name: {row[3]} | Email: {row[4]} | Active: {row[8]}")
        
        # Show Employees
        print("\n👤 EMPLOYEES")
        print("=" * 50)
        cursor.execute("SELECT * FROM employees ORDER BY created_at DESC")
        employees = cursor.fetchall()
        for row in employees:
            print(f"ID: {row[0]} | Name: {row[1]} | Department: {row[2]} | Created: {row[3]}")
        
        # Show Violations
        print("\n🚨 VIOLATIONS")
        print("=" * 50)
        cursor.execute("SELECT * FROM violations ORDER BY timestamp DESC LIMIT 10")
        violations = cursor.fetchall()
        for row in violations:
            print(f"ID: {row[0]} | Employee: {row[2]} | Missing PPE: {row[3]} | Time: {row[5]} | Notified: {row[6]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_data()