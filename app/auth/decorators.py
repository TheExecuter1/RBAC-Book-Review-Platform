from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.auth.models import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.role != 'admin':
            return jsonify(msg="Administrators only!"), 403

        return fn(*args, **kwargs)
    return wrapper
