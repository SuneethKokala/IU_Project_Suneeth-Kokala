from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/')
@app.route('/api')
@app.route('/api/')
def home():
    return '''
    <h1>Safety Monitoring System</h1>
    <p>Dashboard deployed on Vercel</p>
    <p>Note: Camera functionality requires local deployment</p>
    '''

# Vercel handler
def handler(request):
    return app(request.environ, lambda status, headers: None)