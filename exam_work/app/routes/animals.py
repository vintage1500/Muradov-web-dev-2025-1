from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.repositories.animal_repository import get_animals_paginated, get_animal_by_id

bp = Blueprint('animals', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = get_animals_paginated(page)
    return render_template('index.html', animals=pagination.items, pagination=pagination)

@bp.route('/animals/<int:animal_id>')
def animal_detail(animal_id):
    animal = get_animal_by_id(animal_id)
    return render_template('animal/detail.html', animal=animal)
