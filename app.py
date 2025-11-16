from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Copy the dashboard HTML from your templates
with open('automated-safety-monitoring/templates/dashboard.html', 'r') as f:
    DASHBOARD_HTML = f.read()

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/violations')
def get_violations():
    return {'history': []}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)