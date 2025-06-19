from datetime import date, datetime
from calendar import SATURDAY, SUNDAY
from decimal import Decimal
from app.models import Order, OrderItem, CartItem, Product
from sqlalchemy.orm import Session 
from sqlalchemy.exc import NoResultFound

class CartRepository:
    def __init__(self, db):
        self.db = db

    def calculate_delivery_fee(self, total_price, delivery_date: date) -> Decimal:
        if total_price > 5000:
            return Decimal(0)
        weekday = delivery_date.weekday()
        if weekday in [SATURDAY - 5, SUNDAY - 5]:  # Saturday = 5, Sunday = 6
            return Decimal(800)
        return Decimal(500)

    def create_order(self, user_id, phone, address, delivery_date: date) -> Order:
        cart_items = self.db.session.execute(
            self.db.select(CartItem).filter_by(user_id=user_id)
        ).scalars().all()

        if not cart_items:
            raise ValueError("Корзина пуста")

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        delivery_fee = self.calculate_delivery_fee(total_price, delivery_date)
        total_with_delivery = total_price + delivery_fee

        order = Order(
            user_id=user_id,
            status='pending',
            type='regular',
            total_price=total_with_delivery,
            expected_delivery_date=delivery_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.session.add(order)
        self.db.session.flush()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            self.db.session.add(order_item)
            self.db.session.delete(item)

        self.db.session.commit()
        return order


    def get_cart_items_for_user(self, user_id):
        return self.db.session.execute(
            self.db.select(CartItem).filter_by(user_id=user_id)
        ).scalars().all()

    def calculate_cart_total(self, cart_items):
        return sum(item.product.price * item.quantity for item in cart_items)

    def add_product_to_cart(self, user_id, product_id):
        product = self.db.session.get(Product, product_id)
        if not product:
            raise NoResultFound("Продукт не найден.")

        cart_item = self.db.session.execute(
            self.db.select(CartItem).filter_by(user_id=user_id, product_id=product_id)
        ).scalar_one_or_none()

        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
            self.db.session.add(cart_item)

        self.db.session.commit()
        return product.name

    def remove_cart_item(self, user_id, item_id):
        item = self.db.session.get(CartItem, item_id)
        if not item:
            raise NoResultFound("Элемент корзины не найден.")
        if item.user_id != user_id:
            raise PermissionError("Нельзя удалить чужой товар.")

        self.db.session.delete(item)
        self.db.session.commit()

    def update_cart_quantity(self, user_id, item_id, action):
        item = self.db.session.get(CartItem, item_id)
        if not item or item.user_id != user_id:
            raise ValueError("Товар не найден или не принадлежит вам")

        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            item.quantity -= 1
            if item.quantity <= 0:
                self.db.session.delete(item)
                self.db.session.commit()
                return

        self.db.session.commit()
