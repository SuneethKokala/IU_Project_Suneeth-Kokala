# dashboard.py - Supervisor Dashboard
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime
import threading
import pandas as pd
from io import BytesIO

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.database import DatabaseManager

app = Flask(__name__, template_folder='../../templates')
app.secret_key = 'safety_monitoring_secret_key'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Enable CORS for React frontend
CORS(app, supports_credentials=True, origins=['http://localhost:3000'], 
     allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Database manager
db_manager = DatabaseManager()

# Fallback authentication
SUPERVISOR_USERNAME = "supervisor"
SUPERVISOR_PASSWORD = "admin123"

# Global variables for real-time data
violation_history = []
camera_process = None

def load_violations():
    """Load violations from database or log file"""
    global violation_history
    try:
        if db_manager.connected:
            # Load from database
            violations = db_manager.get_violations()
            violation_history = []
            for v in violations:
                violation_history.append({
                    'timestamp': v.timestamp.isoformat(),
                    'employee_id': v.employee_id,
                    'employee_name': v.employee_name,
                    'missing_ppe': json.loads(v.missing_ppe),
                    'location': v.location,
                    'notified': v.notified
                })
        else:
            # Fallback to file
            log_path = 'data/logs/ppe_violations.log'
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    violation_history = [json.loads(line.strip()) for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading violations: {e}")

@app.route('/')
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    # Handle both form data and JSON
    if request.is_json or request.content_type == 'application/json':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
    else:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
    
    print(f"Login attempt - Username: '{username}', Password: '{password}'")
    print(f"Expected - Username: '{SUPERVISOR_USERNAME}', Password: '{SUPERVISOR_PASSWORD}'")
    
    # Try database authentication first
    supervisor = None
    if db_manager.connected:
        supervisor = db_manager.authenticate_supervisor(username, password)
    
    # Fallback to hardcoded credentials
    if supervisor or (username == SUPERVISOR_USERNAME and password == SUPERVISOR_PASSWORD):
        session['logged_in'] = True
        session['supervisor_name'] = supervisor.name if supervisor else 'Default Supervisor'
        session['supervisor_username'] = username
        session.permanent = False
        
        # Return JSON response for API calls
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return redirect(url_for('dashboard'))
    else:
        # Return JSON error for API calls
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        else:
            return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    load_violations()
    return render_template('dashboard.html')

@app.route('/api/violations')
def get_violations():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    load_violations()
    return jsonify({
        'history': violation_history[-100:]  # Last 100 violations
    })

@app.route('/api/mark_notified', methods=['POST'])
def mark_notified():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        violation_index = data.get('index')
        
        if violation_index is None:
            return jsonify({'error': 'Missing violation index'}), 400
        
        load_violations()
        
        if 0 <= violation_index < len(violation_history):
            violation_history[violation_index]['notified'] = True
            violation_history[violation_index]['notified_at'] = datetime.now().isoformat()
            
            # Save updated violations back to file
            os.makedirs('data/logs', exist_ok=True)
            with open('data/logs/ppe_violations.log', 'w') as f:
                for violation in violation_history:
                    f.write(json.dumps(violation) + '\n')
            
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid violation index'}), 400
            
    except Exception as e:
        print(f"Mark notified error: {e}")
        return jsonify({'error': 'Failed to mark as notified'}), 500

@app.route('/api/start_camera', methods=['POST'])
def start_camera():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global camera_process
    try:
        import subprocess
        
        # Get the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Start camera detection using subprocess
        camera_process = subprocess.Popen(
            ['python3', 'run.py', 'camera'],
            cwd=project_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        return jsonify({'success': True, 'message': 'Camera detection started'})
        
    except Exception as e:
        print(f"Camera start error: {e}")
        return jsonify({'error': f'Failed to start camera: {str(e)}'}), 500

@app.route('/api/stop_camera', methods=['POST'])
def stop_camera():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global camera_process
    try:
        import signal
        import subprocess
        
        # Kill all python processes running camera
        subprocess.run(['pkill', '-f', 'run.py camera'], check=False)
        
        if camera_process and camera_process.poll() is None:
            camera_process.kill()
            camera_process.wait(timeout=3)
        
        camera_process = None
        return jsonify({'success': True, 'message': 'Camera detection stopped'})
        
    except Exception as e:
        print(f"Camera stop error: {e}")
        return jsonify({'error': f'Failed to stop camera: {str(e)}'}), 500

@app.route('/api/clear_data', methods=['POST'])
def clear_data():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global violation_history
    try:
        # Clear database if connected
        if db_manager.connected:
            db_manager.clear_violations()
        
        # Clear log file
        log_path = 'data/logs/ppe_violations.log'
        if os.path.exists(log_path):
            open(log_path, 'w').close()
        
        # Clear in-memory data
        violation_history = []
        
        return jsonify({'success': True, 'message': 'All violation data cleared'})
        
    except Exception as e:
        print(f"Clear data error: {e}")
        return jsonify({'error': f'Failed to clear data: {str(e)}'}), 500

@app.route('/api/sync_to_database', methods=['POST'])
def sync_to_database():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        import sys
        sys.path.append('..')
        from app.database_service import DatabaseService
        
        db_service = DatabaseService()
        success, message = db_service.sync_log_to_database()
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/view_database')
def view_database():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        import sys
        sys.path.append('..')
        from app.database_service import DatabaseService
        
        db_service = DatabaseService()
        data = db_service.get_violations_from_db()
        
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export_excel')
def export_excel():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        load_violations()
        
        if not violation_history:
            return jsonify({'error': 'No violations to export'}), 400
        
        # Prepare data for Excel
        excel_data = []
        for violation in violation_history:
            # Parse timestamp
            timestamp = datetime.fromisoformat(violation['timestamp'].replace('Z', '+00:00'))
            
            # Check notification status
            notified = violation.get('notified', False)
            notified_at = violation.get('notified_at', '')
            
            excel_data.append({
                'Date': timestamp.strftime('%Y-%m-%d'),
                'Time': timestamp.strftime('%H:%M:%S'),
                'Employee ID': violation['employee_id'],
                'Employee Name': violation['employee_name'],
                'Missing PPE': ', '.join(violation['missing_ppe']),
                'Location': violation.get('location', 'Main Camera'),
                'Severity': 'High' if len(violation['missing_ppe']) > 1 else 'Medium',
                'Employee Notified': 'Yes' if notified else 'No',
                'Notified At': datetime.fromisoformat(notified_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if notified_at else ''
            })
        
        # Create DataFrame
        df = pd.DataFrame(excel_data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='PPE Violations', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['PPE Violations']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        # Generate filename with current date
        filename = f"PPE_Violations_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"Excel export error: {e}")
        return jsonify({'error': 'Failed to generate Excel file'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data/logs', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=4000)