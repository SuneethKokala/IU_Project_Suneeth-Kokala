from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Dashboard HTML template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Safety Monitoring Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px;
        }
        .header { 
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            color: #333; 
            padding: 25px 30px; 
            border-radius: 15px; 
            margin-bottom: 30px; 
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .header h1 { font-size: 2.2em; font-weight: 300; color: #007bff; }
        .alert { 
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
            color: #856404;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(15px);
            padding: 30px; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        }
        .stat-icon { font-size: 2.5em; margin-bottom: 15px; color: #007bff; }
        .stat-number { font-size: 2.5em; font-weight: bold; margin-bottom: 10px; color: #007bff; }
        .stat-label { color: #666; font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-shield-alt"></i> Safety Monitoring Dashboard</h1>
            <p>Industrial PPE Compliance System</p>
        </div>

        <div class="alert">
            <i class="fas fa-info-circle"></i>
            <strong>Demo Version:</strong> This is a web-deployed version. Camera functionality requires local deployment.
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-hard-hat"></i></div>
                <div class="stat-number">PPE</div>
                <div class="stat-label">Detection System</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-video"></i></div>
                <div class="stat-number">Real-time</div>
                <div class="stat-label">Monitoring</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-bell"></i></div>
                <div class="stat-number">Instant</div>
                <div class="stat-label">Alerts</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

# Vercel handler
def handler(environ, start_response):
    return app(environ, start_response)