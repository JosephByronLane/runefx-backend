from rest_framework.views import exception_handler
import traceback

def custom_exception_handler(exc, context):
    # First, get the standard error response
    response = exception_handler(exc, context)
    
    # Now print detailed information about the exception
    print(f"Exception type: {type(exc)}")
    print(f"Exception message: {str(exc)}")
    print(f"View: {context.get('view').__class__.__name__}")
    print(f"Request path: {context.get('request').path}")
    print(f"Request method: {context.get('request').method}")
    print(f"Request data: {context.get('request').data}")
    print("Traceback:")
    traceback.print_exc()
    
    return response
