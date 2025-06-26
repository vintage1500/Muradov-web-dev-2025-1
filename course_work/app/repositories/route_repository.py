from sqlalchemy import func
from course_work.app.models import Category, Product
from flask import abort, url_for

class RouteRepository:
    def __init__(self, db):
        self.db = db

    def get_category_cards(self):
        # Названия категорий и картинки
        category_map = {
            "Электрогитары": "https://rockdale.ru/upload/iblock/e2e/auumor6cwcg0r2v1nwo65chaibyyhm95/A1216552241142.jpg",
            "Акустические гитары": "https://rockdale.ru/upload/iblock/2d4/267mzjk88lmt3t7i53hseh1qclzrvyve/A1582003255831.jpg",
            "Бас-гитары": "https://rockdale.ru/upload/iblock/af2/0b5159536qx56pyrfkbbu5legpb6iwuv/A1291952435571.jpeg",
        }

        all_categories = self.db.session.query(Category).all()
        category_name_to_id = {c.name: c.id for c in all_categories}

        category_counts = dict(
            self.db.session.query(Category.id, func.count(Product.id))
            .join(Product)
            .group_by(Category.id)
            .all()
        )

        cards = []
        for name, image in category_map.items():
            cid = category_name_to_id.get(name)
            if cid:
                cards.append({
                    "name": name,
                    "image": image,
                    "count": category_counts.get(cid, 0),
                    "link": url_for('catalog.catalog', category=cid)
                })

        # Аксессуары
        accessory_names = ['Чехлы', 'Струны', 'Тюнеры', 'Каподастры', 'Ремни']
        accessory_ids = [category_name_to_id[n] for n in accessory_names if n in category_name_to_id]
        accessory_count = sum(category_counts.get(cid, 0) for cid in accessory_ids)

        cards.append({
            "name": "Аксессуары",
            "image": "https://diezshop.ru/d/alice_a007ksl_kapodastr_dlya_akusticheskoj_gitary_s_mediatorom4.webp",
            "count": accessory_count,
            "link": url_for('catalog.catalog', category=accessory_ids)
        })

        return cards

    def get_product_with_details(self, product_id):
        product = self.db.session.get(Product, product_id)
        if not product:
            abort(404)

        category_name = product.category.name if product.category else ""

        if category_name in ['Электрогитары', 'Акустические гитары', 'Бас-гитары', 'Укулеле', 'Классические гитары']:
            _ = product.guitar_details
        else:
            _ = product.accessory_details

        return product