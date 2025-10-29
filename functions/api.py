"""
Netlify Functions handler for Flask app
"""
from main import app
import serverless_wsgi

def handler(event, context):
    """Netlify Functions handler using serverless-wsgi"""
    return serverless_wsgi.handle_request(app, event, context)
