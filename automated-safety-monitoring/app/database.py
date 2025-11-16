from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os
import sys
sys.path.append('..')
from config.settings import DATABASE_URL, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Supervisor(Base):
    __tablename__ = 'supervisors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    active = Column(Boolean, default=True)

class Violation(Base):
    __tablename__ = 'violations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, nullable=False)
    employee_name = Column(String, nullable=False)
    missing_ppe = Column(Text, nullable=False)  # JSON string
    location = Column(String, default="Main Camera")
    timestamp = Column(DateTime, default=datetime.utcnow)
    notified = Column(Boolean, default=False)
    supervisor_notified = Column(String)  # supervisor username

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.connected = False
        self._connect()
    
    def _connect(self):
        try:
            # Try to connect to PostgreSQL
            db_url = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
            self.engine = create_engine(db_url)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Test connection
            from sqlalchemy import text
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Create tables
            Base.metadata.create_all(bind=self.engine)
            self.connected = True
            print("✅ Connected to PostgreSQL database")
            
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            print("📝 Using file-based logging as fallback")
            self.connected = False
    
    def get_session(self):
        if self.connected:
            return self.SessionLocal()
        return None
    
    def log_violation(self, employee_id, employee_name, missing_ppe, location="Main Camera"):
        if self.connected:
            session = self.get_session()
            try:
                violation = Violation(
                    employee_id=employee_id,
                    employee_name=employee_name,
                    missing_ppe=json.dumps(missing_ppe),
                    location=location
                )
                session.add(violation)
                session.commit()
                print(f"🚨 VIOLATION LOGGED TO DB: {employee_name} missing {', '.join(missing_ppe)}")
                return violation
            except Exception as e:
                print(f"❌ Database logging failed: {e}")
                session.rollback()
                return None
            finally:
                session.close()
        return None
    
    def get_violations(self, limit=100):
        if self.connected:
            session = self.get_session()
            try:
                violations = session.query(Violation).order_by(Violation.timestamp.desc()).limit(limit).all()
                return violations
            except Exception as e:
                print(f"❌ Failed to fetch violations: {e}")
                return []
            finally:
                session.close()
        return []
    
    def add_employee(self, employee_id, name, department=None):
        if self.connected:
            session = self.get_session()
            try:
                employee = Employee(id=employee_id, name=name, department=department)
                session.add(employee)
                session.commit()
                print(f"👤 Employee added: {name}")
                return employee
            except Exception as e:
                print(f"❌ Failed to add employee: {e}")
                session.rollback()
                return None
            finally:
                session.close()
        return None
    
    def add_supervisor(self, username, password, name, email=None, department=None):
        if self.connected:
            session = self.get_session()
            try:
                supervisor = Supervisor(
                    username=username,
                    password=password,
                    name=name,
                    email=email,
                    department=department
                )
                session.add(supervisor)
                session.commit()
                print(f"👨‍💼 Supervisor added: {name}")
                return supervisor
            except Exception as e:
                print(f"❌ Failed to add supervisor: {e}")
                session.rollback()
                return None
            finally:
                session.close()
        return None
    
    def authenticate_supervisor(self, username, password):
        if self.connected:
            session = self.get_session()
            try:
                supervisor = session.query(Supervisor).filter(
                    Supervisor.username == username,
                    Supervisor.password == password,
                    Supervisor.active == True
                ).first()
                
                if supervisor:
                    # Update last login
                    supervisor.last_login = datetime.utcnow()
                    session.commit()
                    return supervisor
                return None
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                return None
            finally:
                session.close()
        return None
    
    def get_supervisors(self):
        if self.connected:
            session = self.get_session()
            try:
                supervisors = session.query(Supervisor).filter(Supervisor.active == True).all()
                return supervisors
            except Exception as e:
                print(f"❌ Failed to fetch supervisors: {e}")
                return []
            finally:
                session.close()
        return []