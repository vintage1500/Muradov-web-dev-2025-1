from sqlalchemy import func
from course_work.app.models import Category, Product
from flask import abort, url_for

class RouteRepository:
    def __init__(self, db):
        self.db = db

    def get_category_cards(self):
        category_map = {
            "Электрогитары": {"id": 1, "image": "https://rockdale.ru/upload/iblock/e2e/auumor6cwcg0r2v1nwo65chaibyyhm95/A1216552241142.jpg"},
            "Акустические гитары": {"id": 2, "image": "https://rockdale.ru/upload/iblock/2d4/267mzjk88lmt3t7i53hseh1qclzrvyve/A1582003255831.jpg"},
            "Бас-гитары": {"id": 3, "image": "https://rockdale.ru/upload/iblock/af2/0b5159536qx56pyrfkbbu5legpb6iwuv/A1291952435571.jpeg"},
        }

        accessory_ids = [4, 5, 6]

        category_counts = dict(
            self.db.session.query(Category.id, func.count(Product.id))
            .join(Product)
            .group_by(Category.id)
            .all()
        )

        cards = []
        for name, data in category_map.items():
            cid = data["id"]
            cards.append({
                "name": name,
                "image": data["image"],
                "count": category_counts.get(cid, 0),
                "link": url_for('catalog.catalog', category=cid)
            })

        # Аксессуары
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

        # Принудительная загрузка деталей (если есть)
        if product.category_id in [1, 2, 3, 4, 5]:  # гитары и укулеле
            _ = product.guitar_details
        else:  # аксессуары
            _ = product.accessory_details

        return product