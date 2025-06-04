from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
import mysql.connector as connector
from .decorators import check_rights
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
    print(type(current_user))  # Должно быть: <class 'app.models.User'> или что-то в этом роде
    print(current_user.__dict__)
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
@check_rights('create')
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
@check_rights('edit')
def edit(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        flash('Пользователя нет в базе данных', 'danger')
        return redirect(url_for('users.index'))
    
    if request.method == 'POST': 
        fields = ('first_name', 'middle_name', 'last_name', 'role_id')
        user_data = { field: request.form.get(field) or None for field in fields }
        if user_data['role_id'] == None:
            user_data['role_id'] = 2
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
                

@bp.route('/<int:user_id>/edit_self', methods=['POST', 'GET'])
@login_required
@check_rights('edit_self')
def edit_self(user_id):
    if current_user.id != user_id:
        flash("Вы можете редактировать только свою учетную запись.", "danger")
        return redirect(url_for('users.index'))

    user = user_repository.get_by_id(user_id)
    if user is None:
        flash('Пользователя нет в базе данных', 'danger')
        return redirect(url_for('users.index'))

    if request.method == 'POST':
        fields = ('first_name', 'middle_name', 'last_name', 'role_id')
        user_data = {field: request.form.get(field) or None for field in fields}
        if user_data['role_id'] == None:
            user_data['role_id'] = 2
        user_data['user_id'] = user_id
        user_data['user_id'] = user_id

        try:
            user_repository.update(**user_data)
            flash('Учетная запись успешно изменена', 'success')
            return redirect(url_for('users.index'))
        except connector.errors.DatabaseError:
            flash('Произошла ошибка при изменении записи', 'danger')
            db.connect().rollback()
            user = user_data

    return render_template('users/edit.html', user_data=user, roles=role_repository.get_all())


@bp.route('/<int:user_id>/delete', methods = ['POST'])
@login_required
@check_rights('delete')
def delete(user_id): 
    user_repository.delete(user_id)
    flash('Учётная запись успешно удалена', 'success')
    return redirect(url_for('users.index'))