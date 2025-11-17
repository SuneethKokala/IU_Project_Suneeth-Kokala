# dashboard.py - Supervisor Dashboard
from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
from flask_cors import CORS
import json
import os
import sys
import signal
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
        import signal
        
        # Kill any existing camera processes first
        try:
            subprocess.run(['pkill', '-f', 'run.py camera'], check=False)
        except:
            pass
        
        # Get the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Start camera detection using subprocess
        camera_process = subprocess.Popen(
            ['python3', 'run.py', 'camera'],
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group
        )
        
        # Give it a moment to start
        import time
        time.sleep(1)
        
        # Check if process is still running
        if camera_process.poll() is None:
            return jsonify({'success': True, 'message': 'PPE detection started successfully'})
        else:
            # Process died immediately, get error
            stdout, stderr = camera_process.communicate()
            error_msg = stderr.decode() if stderr else 'Unknown error'
            return jsonify({'error': f'Detection failed to start: {error_msg}'}), 500
        
    except Exception as e:
        print(f"Camera start error: {e}")
        return jsonify({'error': f'Failed to start detection: {str(e)}'}), 500

@app.route('/api/stop_camera', methods=['POST'])
def stop_camera():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global camera_process
    try:
        import signal
        import subprocess
        
        # Kill all python processes running camera detection
        try:
            subprocess.run(['pkill', '-f', 'run.py camera'], check=False)
        except:
            pass
        
        # Kill the specific process if we have it
        if camera_process and camera_process.poll() is None:
            try:
                # Kill the entire process group
                os.killpg(os.getpgid(camera_process.pid), signal.SIGTERM)
                camera_process.wait(timeout=3)
            except:
                # Force kill if graceful termination fails
                try:
                    os.killpg(os.getpgid(camera_process.pid), signal.SIGKILL)
                except:
                    pass
        
        camera_process = None
        return jsonify({'success': True, 'message': 'PPE detection stopped successfully'})
        
    except Exception as e:
        print(f"Camera stop error: {e}")
        return jsonify({'error': f'Failed to stop detection: {str(e)}'}), 500

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

@app.route('/api/sync_database', methods=['POST'])
def sync_database():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        load_violations()
        
        if not violation_history:
            return jsonify({'success': True, 'synced_count': 0})
        
        import requests
        
        headers = {
            'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR0eGZ0Y3ZwaWlnZHVzemhtdmR1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzMyOTUxNywiZXhwIjoyMDc4OTA1NTE3fQ.AbHq4q-uY0mS08K40mABYAvn9eOGX6QYfQXDktXvN5s',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR0eGZ0Y3ZwaWlnZHVzemhtdmR1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzMyOTUxNywiZXhwIjoyMDc4OTA1NTE3fQ.AbHq4q-uY0mS08K40mABYAvn9eOGX6QYfQXDktXvN5s',
            'Content-Type': 'application/json'
        }
        
        synced_count = 0
        
        for violation in violation_history:
            data = {
                'timestamp': violation['timestamp'],
                'employee_id': violation['employee_id'],
                'employee_name': violation['employee_name'],
                'missing_ppe': violation['missing_ppe'],
                'location': violation.get('location', 'Main Camera'),
                'notified': violation.get('notified', False)
            }
            
            response = requests.post(
                'https://ttxftcvpiigduszhmvdu.supabase.co/rest/v1/ppe_violations',
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                synced_count += 1
        
        return jsonify({'success': True, 'synced_count': synced_count})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_excel')
def export_excel():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        load_violations()
        
        if not violation_history:
            return jsonify({'error': 'No violations to export'}), 400
        
        print(f"Exporting {len(violation_history)} violations to Excel")
        
        # Prepare data for Excel
        excel_data = []
        for i, violation in enumerate(violation_history):
            try:
                # Parse timestamp safely
                timestamp_str = violation.get('timestamp', '')
                if timestamp_str:
                    # Handle different timestamp formats
                    if 'T' in timestamp_str:
                        # ISO format
                        timestamp_str = timestamp_str.replace('Z', '+00:00')
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str)
                        except:
                            # Fallback parsing
                            timestamp = datetime.strptime(timestamp_str.split('+')[0], '%Y-%m-%dT%H:%M:%S')
                    else:
                        # Try parsing as simple format
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                else:
                    timestamp = datetime.now()
                
                # Get missing PPE safely
                missing_ppe = violation.get('missing_ppe', [])
                if isinstance(missing_ppe, str):
                    try:
                        missing_ppe = json.loads(missing_ppe)
                    except:
                        missing_ppe = [missing_ppe]
                elif not isinstance(missing_ppe, list):
                    missing_ppe = []
                
                # Check notification status
                notified = violation.get('notified', False)
                notified_at = violation.get('notified_at', '')
                
                # Parse notified_at safely
                notified_at_str = ''
                if notified_at:
                    try:
                        if 'T' in notified_at:
                            notified_at = notified_at.replace('Z', '+00:00')
                            notified_dt = datetime.fromisoformat(notified_at)
                        else:
                            notified_dt = datetime.strptime(notified_at, '%Y-%m-%d %H:%M:%S')
                        notified_at_str = notified_dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        notified_at_str = str(notified_at)
                
                excel_data.append({
                    'Date': timestamp.strftime('%Y-%m-%d'),
                    'Time': timestamp.strftime('%H:%M:%S'),
                    'Employee ID': violation.get('employee_id', 'Unknown'),
                    'Employee Name': violation.get('employee_name', 'Unknown'),
                    'Missing PPE': ', '.join(missing_ppe) if missing_ppe else 'None',
                    'Location': violation.get('location', 'Main Camera'),
                    'Severity': 'High' if len(missing_ppe) > 1 else 'Medium' if missing_ppe else 'Low',
                    'Employee Notified': 'Yes' if notified else 'No',
                    'Notified At': notified_at_str
                })
                
            except Exception as row_error:
                print(f"Error processing violation {i}: {row_error}")
                # Add a basic row with error info
                excel_data.append({
                    'Date': datetime.now().strftime('%Y-%m-%d'),
                    'Time': datetime.now().strftime('%H:%M:%S'),
                    'Employee ID': 'ERROR',
                    'Employee Name': f'Error processing row {i}',
                    'Missing PPE': str(row_error),
                    'Location': 'Error',
                    'Severity': 'Error',
                    'Employee Notified': 'No',
                    'Notified At': ''
                })
        
        if not excel_data:
            return jsonify({'error': 'No valid data to export'}), 400
        
        print(f"Prepared {len(excel_data)} rows for Excel export")
        
        # Create DataFrame
        df = pd.DataFrame(excel_data)
        
        # Create Excel file in memory
        output = BytesIO()
        
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='PPE Violations', index=False)
                
                # Get workbook and worksheet for formatting
                try:
                    workbook = writer.book
                    worksheet = writer.sheets['PPE Violations']
                    
                    # Auto-adjust column widths
                    for column in worksheet.columns:
                        max_length = 0
                        column_letter = column[0].column_letter
                        for cell in column:
                            try:
                                if cell.value and len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except:
                                pass
                        adjusted_width = min(max(max_length + 2, 10), 50)
                        worksheet.column_dimensions[column_letter].width = adjusted_width
                except Exception as format_error:
                    print(f"Warning: Could not format Excel file: {format_error}")
                    # Continue without formatting
        
        except Exception as excel_error:
            print(f"Excel creation error: {excel_error}")
            return jsonify({'error': f'Failed to create Excel file: {str(excel_error)}'}), 500
        
        output.seek(0)
        
        # Generate filename with current date
        filename = f"PPE_Violations_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        print(f"Sending Excel file: {filename}")
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"Excel export error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data/logs', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=4000)