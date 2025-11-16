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
        print("👨💼 SUPERVISORS")
        print("=" * 50)
        cursor.execute("SELECT COUNT(*) FROM supervisors")
        count = cursor.fetchone()[0]
        print(f"Total supervisors: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM supervisors")
            supervisors = cursor.fetchall()
            for row in supervisors:
                print(f"Row: {row}")
        
        # Show Employees
        print("\n👤 EMPLOYEES")
        print("=" * 50)
        cursor.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        print(f"Total employees: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            for row in employees:
                print(f"Row: {row}")
        
        # Show Violations
        print("\n🚨 VIOLATIONS")
        print("=" * 50)
        cursor.execute("SELECT COUNT(*) FROM violations")
        count = cursor.fetchone()[0]
        print(f"Total violations: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM violations LIMIT 5")
            violations = cursor.fetchall()
            for row in violations:
                print(f"Row: {row}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_data()