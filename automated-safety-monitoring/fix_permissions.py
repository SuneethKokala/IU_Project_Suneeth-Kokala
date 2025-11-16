#!/usr/bin/env python3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config.settings import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER

def fix_permissions():
    try:
        # Connect as postgres admin
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user='postgres',
            password=input("Enter PostgreSQL admin password: "),
            database=DATABASE_NAME
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Grant all permissions on all tables
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {DATABASE_USER};")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {DATABASE_USER};")
        cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {DATABASE_USER};")
        cursor.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO {DATABASE_USER};")
        
        print("✅ Permissions fixed!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_permissions()