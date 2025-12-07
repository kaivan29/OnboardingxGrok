from app import app
from vercel_wsgi import handle


def handler(event, context):
    # Vercel entrypoint: adapts Flask app to serverless request/response.
    return handle(app, event, context)
