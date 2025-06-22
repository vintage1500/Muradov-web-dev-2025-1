from app.extensions import db
from app.models import Animal, Photo

def get_animals_paginated(page, per_page=10):
    return Animal.query.order_by(Animal.status.desc(), Animal.created_at.desc()).paginate(page=page, per_page=per_page)

def get_animal_by_id(animal_id):
    return Animal.query.get_or_404(animal_id)

def create_animal(data, photos):
    animal = Animal(**data)
    db.session.add(animal)
    db.session.flush()
    for file in photos:
        photo = Photo(filename=file['filename'], mime_type=file['mime'], animal_id=animal.id)
        db.session.add(photo)
    db.session.commit()
    return animal

def delete_animal(animal_id):
    animal = get_animal_by_id(animal_id)
    db.session.delete(animal)
    db.session.commit()
