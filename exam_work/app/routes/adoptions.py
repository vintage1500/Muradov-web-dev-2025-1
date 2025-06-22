from flask import Blueprint, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.repositories.adoption_repository import AdoptionRepository

bp = Blueprint('adoptions', __name__, url_prefix='/adoptions')
adoption_repo = AdoptionRepository(db)

@bp.route('/request/<int:animal_id>', methods=['POST'])
@login_required
def send_adoption_request(animal_id):
    contact_info = request.form.get('contact_info')
    try:
        adoption_repo.create_adoption_request(animal_id, current_user.id, contact_info)
        flash('Заявка отправлена.', 'success')
    except Exception:
        db.session.rollback()
        flash('Ошибка при отправке заявки.', 'danger')
    return redirect(url_for('animals.animal_detail', animal_id=animal_id))

@bp.route('/accept/<int:adoption_id>', methods=['POST'])
@login_required
def accept_adoption(adoption_id):
    if current_user.role.name not in ['admin', 'moderator']:
        flash('У вас недостаточно прав.', 'danger')
        return redirect(url_for('animals.index'))

    try:
        adoption_repo.accept_adoption(adoption_id)
        flash('Заявка одобрена.', 'success')
    except Exception:
        db.session.rollback()
        flash('Ошибка при одобрении заявки.', 'danger')

    return redirect(request.referrer or url_for('animals.index'))

@bp.route('/reject/<int:adoption_id>', methods=['POST'])
@login_required
def reject_adoption(adoption_id):
    if current_user.role.name not in ['admin', 'moderator']:
        flash('У вас недостаточно прав.', 'danger')
        return redirect(url_for('animals.index'))

    try:
        adoption_repo.reject_adoption(adoption_id)
        flash('Заявка отклонена.', 'success')
    except Exception:
        db.session.rollback()
        flash('Ошибка при отклонении заявки.', 'danger')

    return redirect(request.referrer or url_for('animals.index'))