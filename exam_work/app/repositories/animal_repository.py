from exam_work.app.models import Animal, Photo

class AnimalRepository:
    def __init__(self, db):
        self.db = db

    def get_animals_paginated(self, page, per_page=10):
        return Animal.query.order_by(Animal.status.desc(), Animal.created_at.desc()).paginate(page=page, per_page=per_page)

    def get_animal_by_id(self, animal_id):
        return Animal.query.get_or_404(animal_id)

    def create_animal(self, data, photos):
        animal = Animal(**data)
        self.db.session.add(animal)
        self.db.session.flush()
        for file in photos:
            photo = Photo(filename=file['filename'], mime_type=file['mime'], animal_id=animal.id)
            self.db.session.add(photo)
        self.db.session.commit()
        return animal

    def delete_animal(self, animal_id):
        animal = self.get_animal_by_id(animal_id)
        self.db.session.delete(animal)
        self.db.session.commit()

        