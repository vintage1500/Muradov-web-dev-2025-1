from course_work.app.models import AccessoryDetail, Product, Category, Brand, Order, GuitarDetail, OrderItem


class AdminRepository:
    def __init__(self, db):
        self.db = db

    # -------- Products --------

    def get_all_products(self):
        return Product.query.all()

    def get_product_by_id(self, product_id):
        return Product.query.get(product_id)

    def add_full_product(self, product_data, guitar_data=None, accessory_data=None):
        product = Product(
            name=product_data["name"],
            description=product_data.get("description"),
            price=product_data["price"],
            sku=product_data["sku"],
            stock_quantity=product_data["stock_quantity"],
            category_id=product_data["category_id"],
            brand_id=product_data["brand_id"],
            image_url=product_data.get("image_url", "default.jpg")
        )
        self.db.session.add(product)
        self.db.session.flush()  # получаем product.id

        if guitar_data:
            self.db.session.add(GuitarDetail(
                product_id=product.id,
                type=guitar_data.get("type"),
                strings_number=guitar_data.get("strings_number"),
                body_material=guitar_data.get("body_material"),
                neck_material=guitar_data.get("neck_material"),
                pickups=guitar_data.get("pickups")
            ))

        if accessory_data:
            self.db.session.add(AccessoryDetail(
                product_id=product.id,
                compatibility=accessory_data.get("compatibility"),
                material=accessory_data.get("material"),
                color=accessory_data.get("color")
            ))

        self.db.session.commit()
        return product
    
    def update_full_product(self, product, product_data, guitar_data=None, accessory_data=None):
        # Обновляем поля
        product.name = product_data["name"]
        product.description = product_data.get("description")
        product.price = product_data["price"]
        product.sku = product_data["sku"]
        product.stock_quantity = product_data["stock_quantity"]
        product.category_id = product_data["category_id"]
        product.brand_id = product_data["brand_id"]
        product.image_url = product_data.get("image_url", product.image_url)

        # Гитара
        if guitar_data:
            if product.guitar_details:
                gd = product.guitar_details
                gd.type = guitar_data.get("type")
                gd.strings_number = guitar_data.get("strings_number")
                gd.body_material = guitar_data.get("body_material")
                gd.neck_material = guitar_data.get("neck_material")
                gd.pickups = guitar_data.get("pickups")
            else:
                self.db.session.add(GuitarDetail(
                    product_id=product.id,
                    **guitar_data
                ))

        # Аксессуар
        if accessory_data:
            if product.accessory_details:
                ad = product.accessory_details
                ad.compatibility = accessory_data.get("compatibility")
                ad.material = accessory_data.get("material")
                ad.color = accessory_data.get("color")
            else:
                self.db.session.add(AccessoryDetail(
                    product_id=product.id,
                    **accessory_data
                ))

        # Попробуем обновить статусы заказов, если пополнился склад
        if product.stock_quantity > 0:
            self.try_fulfill_backorders(product)

        self.db.session.commit()
        return product

    def try_fulfill_backorders(self, product: Product):
    # Получаем заказы, ожидающие поставки, отсортированные по дате
        waiting_orders = (
            self.db.session.query(Order)
            .join(Order.items)
            .filter(Order.status == 'waiting_for_stock')
            .filter(OrderItem.product_id == product.id)
            .order_by(Order.created_at.asc())
            .all()
        )

        for order in waiting_orders:
            can_fulfill = True

            for item in order.items:
                if item.product_id == product.id:
                    if product.stock_quantity < item.quantity:
                        can_fulfill = False
                        break

            if can_fulfill:
                # Обновляем заказ
                order.status = 'pending'
                for item in order.items:
                    if item.product_id == product.id:
                        product.stock_quantity -= item.quantity

                        # Защита от отрицательного остатка
                        if product.stock_quantity < 0:
                            product.stock_quantity = 0

        self.db.session.commit()

    def delete_product(self, product):
        self.db.session.delete(product)
        self.db.session.commit()

    # -------- Orders --------

    def get_all_orders(self):
        return Order.query.order_by(Order.created_at.desc()).all()

    def get_recent_orders(self, limit=5):
        return Order.query.order_by(Order.created_at.desc()).limit(limit).all()

    def get_order_by_id(self, order_id):
        return Order.query.get(order_id)

    def update_order_status(self, order, status):
        order.status = status
        self.db.session.commit()
        return order

    # -------- Categories & Brands --------

    def get_all_categories(self):
        return Category.query.all()

    def get_all_brands(self):
        return Brand.query.all()
    
    def get_category_ids_by_names(self, names: list[str]) -> list[int]:
        return [
            c.id for c in Category.query.filter(Category.name.in_(names)).all()
        ]

    
