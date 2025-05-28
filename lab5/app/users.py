from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
import mysql.connector as connector

from .repositories import UserRepository, RoleRepository
from .extension import db

user_repository = UserRepository(db)
role_repository = RoleRepository(db)

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.errorhandler(connector.errors.DatabaseError)
def handler():
    pass

@bp.route('/')
def index():
    return render_template('users/index.html', users=user_repository.all())

@bp.route('/<int:user_id>')
def show(user_id):
    user = user_repository.get_by_id(user_id)
    if not user:  
        flash('Пользователя нет в базе данных', 'danger')
        return redirect(url_for('users.index'))
    
    user_role = None
    if user.role_id:  
        user_role = role_repository.get_by_id(user.role_id)  
        
    return render_template('users/show.html', 
                         user_data=user,
                         user_role=user_role)

@bp.route('/new', methods= ['POST', 'GET'])
@login_required
def new():
    user_data = {}
    if request.method == 'POST':
        fields = ('username', 'password', 'first_name', 'middle_name', 'last_name', 'role_id')
        user_data = { field: request.form.get(field) or None for field in fields }
        try:
            user_repository.create(**user_data)
            flash('Учётная запись успешно создана', 'success')
            return redirect(url_for('users.index'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при создании записи. Проверьте, что все необходимые поля заполнены', 'danger')
            db.connect().rollback()
    return render_template('users/new.html', user_data=user_data, roles=role_repository.get_all())


@bp.route('/<int:user_id>/edit', methods = ['POST', 'GET'])
@login_required
def edit(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        flash('Пользователя нет в базе данных', 'danger')
        return redirect(url_for('users.index'))
    
    if request.method == 'POST':
        fields = ('first_name', 'middle_name', 'last_name', 'role_id')
        user_data = { field: request.form.get(field) or None for field in fields }
        user_data['user_id'] = user_id
        try:
            user_repository.update(**user_data)
            flash('Учетная запись успешно измененена', 'success')
            return redirect(url_for('users.index'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при изменении записи', 'danger')
            db.connect().rollback()
            user = user_data
    return render_template('users/edit.html', user_data=user, roles=role_repository.get_all())
            

@bp.route('/<int:user_id>/delete', methods = ['POST'])
@login_required
def delete(user_id): 
    user_repository.delete(user_id)
    flash('Учётная запись успешно удалена', 'success')
    return redirect(url_for('users.index'))