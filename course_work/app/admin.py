from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .extension import db
from .decorators import admin_required
from .repositories.admin_repository import AdminRepository

admin_repo = AdminRepository(db)

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
@admin_required
def dashboard():
    orders = admin_repo.get_recent_orders()
    return render_template('admin/dashboard.html', orders=orders)

@bp.route('/products')
@login_required
@admin_required
def products():
    products = admin_repo.get_all_products()
    return render_template('admin/products.html', products=products)

@bp.route('/orders')
@login_required
@admin_required
def orders():
    orders = admin_repo.get_all_orders()
    return render_template('admin/orders.html', orders=orders)

@bp.route('/order/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = admin_repo.get_order_by_id(order_id)
    new_status = request.form.get('status')
    admin_repo.update_order_status(order, new_status)
    flash('Статус заказа обновлён.', 'success')
    return redirect(url_for('admin.orders'))

@bp.route('/users')
@login_required
@admin_required
def users():
    from .repositories.user_repository import UserRepository
    user_repo = UserRepository(db)
    users = user_repo.get_all_users()
    return render_template('admin/users.html', users=users)
        

@bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    admin_repo = AdminRepository(db)

    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        cat_is_guitar = category_id in [1, 2, 3, 4, 5]
        cat_is_accessory = category_id in [6, 7, 8, 9, 10]

        product_data = {
            "name": request.form['name'],
            "description": request.form.get('description'),
            "price": request.form.get('price', type=float),
            "sku": request.form['sku'],
            "stock_quantity": request.form.get('stock_quantity', type=int),
            "category_id": category_id,
            "brand_id": request.form.get('brand_id', type=int),
            "image_url": "default.jpg"
        }

        guitar_data = None
        accessory_data = None

        if cat_is_guitar:
            guitar_data = {
                "type": request.form.get('guitar_type'),
                "strings_number": request.form.get('strings_number', type=int),
                "body_material": request.form.get('body_material'),
                "neck_material": request.form.get('neck_material'),
                "pickups": request.form.get('pickups')
            }

        if cat_is_accessory:
            accessory_data = {
                "compatibility": request.form.get('compatibility'),
                "material": request.form.get('material'),
                "color": request.form.get('color')
            }

        admin_repo.add_full_product(product_data, guitar_data, accessory_data)
        flash("Товар успешно добавлен", "success")
        return redirect(url_for('admin.add_product'))

    categories = admin_repo.get_all_categories()
    brands = admin_repo.get_all_brands()
    return render_template("admin/add_edit_product.html", categories=categories, brands=brands)


@bp.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    admin_repo = AdminRepository(db)
    product = admin_repo.get_product_by_id(product_id)
    categories = admin_repo.get_all_categories()
    brands = admin_repo.get_all_brands()

    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        cat_is_guitar = category_id in [1, 2, 3, 4, 5]
        cat_is_accessory = category_id in [6, 7, 8, 9, 10]

        product_data = {
            "name": request.form['name'],
            "description": request.form.get('description'),
            "price": request.form.get('price', type=float),
            "sku": request.form['sku'],
            "stock_quantity": request.form.get('stock_quantity', type=int),
            "category_id": category_id,
            "brand_id": request.form.get('brand_id', type=int),
            "image_url": "default.jpg"
        }

        guitar_data = None
        accessory_data = None

        if cat_is_guitar:
            guitar_data = {
                "type": request.form.get('guitar_type'),
                "strings_number": request.form.get('strings_number', type=int),
                "body_material": request.form.get('body_material'),
                "neck_material": request.form.get('neck_material'),
                "pickups": request.form.get('pickups')
            }

        if cat_is_accessory:
            accessory_data = {
                "compatibility": request.form.get('compatibility'),
                "material": request.form.get('material'),
                "color": request.form.get('color')
            }

        admin_repo.update_full_product(product, product_data, guitar_data, accessory_data)
        flash("Товар успешно обновлён", "success")
        return redirect(url_for('admin.edit_product', product_id=product.id))

    return render_template("admin/add_edit_product.html",
                           product=product,
                           categories=categories,
                           brands=brands)

@bp.route('/admin/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = admin_repo.get_product_by_id(product_id)
    if not product:
        flash("Товар не найден", "danger")
        return redirect(url_for("admin.products"))

    admin_repo.delete_product(product)
    flash("Товар успешно удалён", "success")
    return redirect(url_for("admin.products"))