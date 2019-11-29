# -- coding: utf-8 --
import JsonResponse
import json

SSL = True

def rerror(ex, status_code=400):  # response error
    r = JsonResponse.JsonResponse()
    r.status_code = status_code

    if isinstance(ex, Exception):
        name = type(ex).__name__
        msg = str(ex)
    elif isinstance(ex, str):
        name = "ValueError"
        msg = ex
    else:
        raise ValueError("'ex' argument must be 'str' or 'Exception'")

    r.data = json.dumps({
        'error': name,
        'message': msg
    })
    return r

