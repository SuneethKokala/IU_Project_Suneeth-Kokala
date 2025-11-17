# dashboard_aws.py - AWS optimized dashboard
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import json
import os
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = 'safety_monitoring_secret_key'

# Simple authentication
SUPERVISOR_USERNAME = "supervisor"
SUPERVISOR_PASSWORD = "admin123"

# Global variables for real-time data
current_violations = []
violation_history = []

def load_violations():
    """Load violations from log file"""
    global violation_history
    try:
        if os.path.exists('ppe_violations.log'):
            with open('ppe_violations.log', 'r') as f:
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
    username = request.form['username']
    password = request.form['password']
    
    if username == SUPERVISOR_USERNAME and password == SUPERVISOR_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
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
        'current': current_violations,
        'history': violation_history[-50:]  # Last 50 violations
    })

@app.route('/api/clear_current')
def clear_current():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global current_violations
    current_violations = []
    return jsonify({'success': True})

@app.route('/health')
def health_check():
    """Health check endpoint for AWS"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

def add_violation(employee_id, employee_name, missing_ppe):
    """Add violation to current alerts"""
    global current_violations
    violation = {
        'timestamp': datetime.now().isoformat(),
        'employee_id': employee_id,
        'employee_name': employee_name,
        'missing_ppe': missing_ppe,
        'location': 'AWS Camera'
    }
    current_violations.append(violation)
    
    # Keep only last 10 current violations
    if len(current_violations) > 10:
        current_violations = current_violations[-10:]

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Run on all interfaces for AWS
    app.run(debug=False, host='0.0.0.0', port=4000)