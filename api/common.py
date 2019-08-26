# -- coding: utf-8 --
import JsonResponse
import json

SSL = True

def rerror(ex, status_code=400):  # response error
    r = JsonResponse.JsonResponse()
    r.status_code = status_code
    ex_type = type(ex)

    if ex_type == Exception:
        name = ex_type.__name__,
        msg = str(ex)
    elif ex_type == str:
        name = "ValueError",
        msg = ex
    else:
        raise ValueError("'ex' argument must be 'str' or 'Exception'")

    r.data = json.dumps({
        'error': name,
        'message': msg
    })
    return r

