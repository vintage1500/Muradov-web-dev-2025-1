from flask import Blueprint, render_template, request
from .models import Product, Category, Brand
from .extension import db

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

from flask import request, render_template
from course_work.app.models import Category, Brand
from course_work.app.repositories.catalog_repository import CatalogRepository
from course_work.app.extension import db

catalog_repo = CatalogRepository(db)

@bp.route('/')
def catalog():
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Получаем все параметры
    filters = {
        "query": request.args.get("q", "", type=str),
        "category_ids": request.args.getlist("category", type=int),
        "brand_ids": request.args.getlist("brand", type=int),
        "min_price": request.args.get("min_price", type=float),
        "max_price": request.args.get("max_price", type=float),
        "available": request.args.get("available", type=int)
    }

    pagination = catalog_repo.get_filtered_products(page, per_page, filters)
    products = pagination.items

    categories = Category.query.all()
    brands = Brand.query.all()

    return render_template("catalog/catalog.html",
                           products=products,
                           pagination=pagination,
                           categories=categories,
                           brands=brands,
                           selected_categories=[str(cid) for cid in filters["category_ids"]],
                           selected_brands=[str(bid) for bid in filters["brand_ids"]],
                           min_price=filters["min_price"],
                           max_price=filters["max_price"],
                           query=filters["query"],
                           available=filters["available"])
