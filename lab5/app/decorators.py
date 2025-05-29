from flask import Blueprint, flash, redirect, url_for 
from functools import wraps
from flask_login import current_user

def check_rights(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role_id = current_user.role_id if current_user.is_authenticated else None
            print('\n\n\n' + str(role_id) + '\n\n\n')
            rights = {
                1: {"create", "edit", "view", "delete", "view_logs_all"},
                2: {"edit", "view_self", "view_logs_own"}
            }

            allowed_actions = rights.get(role_id, set())

            if action not in allowed_actions:
                flash("У вас недостаточно прав для доступа к данной странице.", "warning")
                return redirect(url_for("users.index"))  
            return func(*args, **kwargs)
        return wrapper
    return decorator
