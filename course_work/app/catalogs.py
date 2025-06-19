from flask import Blueprint, render_template, request
from .models import Product, Category, Brand
from .extension import db

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@bp.route('/')
def catalog():
    # Параметры пагинации
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Параметры фильтрации
    category_ids = request.args.getlist('category', type=int)
    brand_ids = request.args.getlist('brand', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Product.query

    if category_ids:
        query = query.filter(Product.category_id.in_(category_ids))
    if brand_ids:
        query = query.filter(Product.brand_id.in_(brand_ids))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    pagination = query.paginate(page=page, per_page=per_page)
    products = pagination.items

    categories = Category.query.all()
    brands = Brand.query.all()

    return render_template('catalog/catalog.html',
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           brands=brands,
                           selected_categories=category_ids,
                           selected_brands=brand_ids,
                           min_price=min_price,
                           max_price=max_price)
