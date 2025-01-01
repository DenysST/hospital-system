from functools import wraps
from flask import jsonify
from pydantic import ValidationError

def exception_handler(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    return wrapper