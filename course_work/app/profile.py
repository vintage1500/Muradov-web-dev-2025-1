from flask import Blueprint, render_template
from flask_login import login_required, current_user
from course_work.app.models import Order

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def profile():
    user = current_user
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template('profile.html', user=user, orders=orders)
