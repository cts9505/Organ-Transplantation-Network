"""
WSGI Entry Point for Serverless Deployment
Supports: Vercel, AWS Lambda, Google Cloud Functions, Azure Functions
"""
from main import app

# For Vercel
app = app

# For AWS Lambda (with Zappa or Mangum)
def handler(event, context):
    """AWS Lambda handler"""
    try:
        from mangum import Mangum
        handler = Mangum(app)
        return handler(event, context)
    except ImportError:
        return {
            'statusCode': 500,
            'body': 'Mangum not installed. Run: pip install mangum'
        }

# For Google Cloud Functions
def gcf_handler(request):
    """Google Cloud Functions handler"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

# For Azure Functions
def azure_handler(req):
    """Azure Functions handler"""
    try:
        import azure.functions as func
        from werkzeug.wrappers import Request, Response
        
        request = Request(req.get_body())
        response = Response.from_app(app, request.environ)
        
        return func.HttpResponse(
            response.get_data(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except ImportError:
        return {
            'statusCode': 500,
            'body': 'Azure Functions SDK not installed'
        }
