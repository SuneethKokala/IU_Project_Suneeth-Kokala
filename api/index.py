from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Safety Monitoring System</h1>
    <p>Dashboard deployed on Vercel</p>
    <p>Note: Camera functionality requires local deployment</p>
    '''

# Export for Vercel
handler = app