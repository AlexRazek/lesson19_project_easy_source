from flask import request, abort

# создаем декоратор на ограничение чтения

def check_token(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

