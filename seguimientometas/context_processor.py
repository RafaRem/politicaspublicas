import os

def add_variable_context(request):
    return{
        'api_key':os.getenv('api_key')
    }