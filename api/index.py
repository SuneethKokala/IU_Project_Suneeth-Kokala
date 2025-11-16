from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''
        <h1>Safety Monitoring System</h1>
        <p>Dashboard deployed on Vercel</p>
        <p>Note: Camera functionality requires local deployment</p>
        '''
        
        self.wfile.write(html.encode())