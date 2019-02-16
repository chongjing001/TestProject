import random



from flask import session, redirect, url_for, request
from functools import wraps

from app.models import User

# 方法一
def is_login(func):
    @wraps(func)
    def check_status(*args, **kwargs):
        try:
            session['user_id']
            return func(*args, **kwargs)
        except Exception as e:
            return redirect(url_for('user.login'))

    return check_status



# 方法二
# def is_login(func):
#     @wraps(func)
#     def check_status(*args, **kwargs):
#         if 'user_id' in session:
#             return func(*args,**kwargs)
#         else:
#             return redirect(url_for('user.login'))
#
#     return check_status
