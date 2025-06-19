from flask import Blueprint, render_template, send_from_directory, current_app, abort
from app.repositories import user_repository
from app.models import db 
from app.repositories.route_repository import RouteRepository 
 
bp = Blueprint('main', __name__)


repo = RouteRepository(db)

@bp.route('/')
def index():
    category_cards = repo.get_category_cards()
    return render_template("index.html", category_cards=category_cards)


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = repo.get_product_with_details(product_id)
    return render_template('catalog/product_detail.html', product=product)
