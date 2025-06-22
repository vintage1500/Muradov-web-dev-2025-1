from app.models import Adoption, Animal
from datetime import datetime

class AdoptionRepository:
    def __init__(self, db):
        self.db = db

    def get_adoptions_by_animal(self, animal_id):
        return Adoption.query.filter_by(animal_id=animal_id).order_by(Adoption.created_at.desc()).all()

    def create_adoption_request(self, animal_id, user_id, contact_info):
        adoption = Adoption(
            animal_id=animal_id,
            user_id=user_id,
            contact_info=contact_info,
            status='pending',
            created_at=datetime.utcnow()
        )
        self.db.session.add(adoption)
        self.db.session.commit()
        return adoption

    def accept_adoption(self, adoption_id):
        adoption = Adoption.query.get_or_404(adoption_id)
        adoption.status = 'accepted'
        adoption.animal.status = 'adopted'

        # Все другие заявки переводим в rejected_adopted
        Adoption.query.filter(
            Adoption.animal_id == adoption.animal_id,
            Adoption.id != adoption.id,
            Adoption.status == 'pending'
        ).update({Adoption.status: 'rejected_adopted'})

        self.db.session.commit()

    def reject_adoption(self, adoption_id):
        adoption = Adoption.query.get_or_404(adoption_id)
        adoption.status = 'rejected'
        self.db.session.commit()
