from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
import mysql.connector as connector

from .repositories import UserRepository, RoleRepository
from .extension import db

user_repository = UserRepository(db)
# role_repository = RoleRepository(db)

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def index():
    return render_template('users/index.html', users=user_repository.all())