from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return redirect(url_for('public.home')) # تعديل لتوجيه العميل للصفحة الرئيسية العامة
        return f(*args, **kwargs)
    return decorated