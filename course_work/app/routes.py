from flask import Blueprint, render_template, send_from_directory, current_app, abort
from app.repositories import user_repository
from app.models import db
 
bp = Blueprint('main', __name__)

@bp.route('/')
def index(): 
    return render_template('index.html')