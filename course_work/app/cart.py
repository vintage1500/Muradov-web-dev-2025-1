from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from datetime import datetime, timedelta
from .repositories.cart_repository import CartRepository
from .extension import db

bp = Blueprint('cart', __name__, url_prefix='/cart')
cart_repo = CartRepository(db)

@bp.route('/')
@login_required
def cart():
    items = cart_repo.get_cart_items_for_user(current_user.id)
    total = cart_repo.calculate_cart_total(items)
    return render_template(
        'cart.html',
        cart_items=items,
        total_sum=total,
        datetime=datetime,
        timedelta=timedelta
    )


@bp.route('/remove/<int:item_id>')
@login_required
def remove(item_id):
    try:
        cart_repo.remove_cart_item(current_user.id, item_id)
        flash('Товар удален из корзины.', 'info')
    except PermissionError:
        abort(403)
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('cart.cart'))


@bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    try:
        product_name = cart_repo.add_product_to_cart(current_user.id, product_id)
        flash(f'Добавлен в корзину: {product_name}', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(request.referrer or url_for('catalog.catalog'))

@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    phone = request.form.get('phone')
    address = request.form.get('address')
    date_str = request.form.get('expected_delivery_date')

    if not date_str:
        flash('Укажите дату доставки.', 'danger')
        return redirect(url_for('cart.cart'))

    delivery_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if delivery_date <= datetime.utcnow().date():
        flash('Дата доставки должна быть позже текущей.', 'danger')
        return redirect(url_for('cart.cart'))

    try: 
        cart_repo.create_order(
            user_id=current_user.id,
            phone=phone,
            address=address,
            delivery_date=delivery_date
        )
        flash("Заказ успешно оформлен!", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('cart.cart'))


@bp.route('/update_quantity/<int:item_id>', methods=['POST'])
@login_required
def update_quantity(item_id):
    action = request.form.get('action')
    try:
        cart_repo.update_cart_quantity(current_user.id, item_id, action)
        flash('Количество обновлено', 'info')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('cart.cart'))