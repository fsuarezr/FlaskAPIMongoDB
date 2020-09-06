import json

def generateResponse(options):
    success = options['success']
    data = options['data']
    error = options['error']
    result = {
        'success': success,
        'data': data,
        'error': error
    }
    return json.dumps(result)

def templateSuccess(data):
    result = generateResponse({'success':True, 'data': data, 'error': None})
    return result
    
def templateError(options):
    code = options['code']
    message = options['message']
    error = {
        'code': code,
        'message': message
    }
    result = generateResponse({'success': False, 'data': None, 'error': error})
    return result