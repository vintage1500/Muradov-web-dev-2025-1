from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
import os
import bleach # нужно для безопасной очистки html-контента (экранирует теги например)
from werkzeug.utils import secure_filename # очищает имя загружаемого файла для безопасного хранения
from app.extensions import db
from app.repositories.animal_repository import AnimalRepository

animal_repo = AnimalRepository(db)

bp = Blueprint('animals', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = animal_repo.get_animals_paginated(page)
    return render_template('index.html', animals=pagination.items, pagination=pagination)

@bp.route('/animals/<int:animal_id>')
def animal_detail(animal_id):
    animal = animal_repo.get_animal_by_id(animal_id)
    return render_template('animal/detail.html', animal=animal)

@bp.route('/animals/add', methods=['GET', 'POST'])
@login_required
def add_animal():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для выполнения данного действия.', 'danger')
        return redirect(url_for('animals.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = bleach.clean(request.form.get('description'), tags=[], attributes={})
        age_months = request.form.get('age_months')
        breed = request.form.get('breed')
        gender = request.form.get('gender')
        status = request.form.get('status', 'available')

        images = request.files.getlist('images')

        data = {
            'name': name,
            'description': description,
            'age_months': age_months,
            'breed': breed,
            'gender': gender,
            'status': status
        }

        files_data = []
        for image in images:
            if image.filename:
                filename = secure_filename(image.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                files_data.append({'filename': filename, 'mime': image.mimetype})

        try:
            animal_repo.create_animal(data, files_data)
            flash('Животное успешно добавлено.', 'success')
            return redirect(url_for('animals.index'))
        except Exception:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            return render_template('animal/form.html', animal=data, edit=False)

    return render_template('animal/form.html', edit=False)

@bp.route('/animals/<int:animal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_animal(animal_id):
    animal = animal_repo.get_animal_by_id(animal_id)

    if current_user.role.name not in ('admin', 'moderator'):
        flash('У вас недостаточно прав для выполнения данного действия.', 'danger')
        return redirect(url_for('animals.index'))

    if request.method == 'POST':
        animal.name = request.form.get('name')
        animal.description = bleach.clean(request.form.get('description'), tags=[], attributes={})
        animal.age_months = request.form.get('age_months')
        animal.breed = request.form.get('breed')
        animal.gender = request.form.get('gender')
        animal.status = request.form.get('status')

        try:
            db.session.commit()
            flash('Данные успешно обновлены.', 'success')
            return redirect(url_for('animals.animal_detail', animal_id=animal.id))
        except Exception:
            db.session.rollback()
            flash('Ошибка при сохранении изменений.', 'danger')

    return render_template('animal/form.html', animal=animal, edit=True)

@bp.route('/animals/<int:animal_id>/delete', methods=['POST'])
@login_required
def delete_animal_route(animal_id):
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для выполнения данного действия.', 'danger')
        return redirect(url_for('animals.index'))

    try:
        animal_repo.delete_animal(animal_id)
        flash('Животное успешно удалено.', 'success')
    except Exception:
        db.session.rollback()
        flash('Ошибка при удалении.', 'danger')

    return redirect(url_for('animals.index'))
