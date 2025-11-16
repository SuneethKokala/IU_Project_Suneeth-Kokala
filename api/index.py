from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Read the dashboard HTML
    dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'automated-safety-monitoring', 'templates', 'dashboard.html')
    try:
        with open(dashboard_path, 'r') as f:
            return f.read()
    except:
        return '''
        <h1>🛡️ Safety Monitoring Dashboard</h1>
        <p>Dashboard loading...</p>
        '''

@app.route('/api/violations')
def violations():
    return {'history': []}

# Vercel handler
def handler(environ, start_response):
    return app(environ, start_response)