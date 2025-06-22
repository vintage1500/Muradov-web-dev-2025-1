from app.models import Adoption

class AdoptionRepository:
    def __init__(self, db):
        self.db = db

    def get_adoptions_by_animal(self, animal_id):
        return Adoption.query.filter_by(animal_id=animal_id).order_by(Adoption.created_at.desc()).all()