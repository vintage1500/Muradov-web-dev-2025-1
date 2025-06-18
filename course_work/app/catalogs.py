from flask import Blueprint, render_template, request
from .models import Product, Category, Brand
from .extension import db

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@bp.route('/')
def catalog():
    # Получение параметров
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Фильтры (позже можно добавить фильтрацию по бренду, цене и т.п.)
    category_ids = request.args.getlist('category')
    brand_ids = request.args.getlist('brand')

    query = Product.query

    if category_ids:
        query = query.filter(Product.category_id.in_(category_ids))

    if brand_ids:
        query = query.filter(Product.brand_id.in_(brand_ids))

    # Пагинация
    pagination = query.paginate(page=page, per_page=per_page)
    products = pagination.items

    # Для фильтров
    categories = Category.query.all()
    brands = Brand.query.all()

    return render_template('catalog/catalog.html',
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           brands=brands,
                           selected_categories=category_ids,
                           selected_brands=brand_ids)