from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime
from werkzeug.security import check_password_hash

from .extension import db


class User(db.Model, UserMixin):
    __tablename__ ='users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False) 
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship('CartItem', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='user')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.login}>'


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', backref='brand', lazy=True)

    def __repr__(self):
        return f'<Brand {self.name}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    image_url = db.Column(db.String(255)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sku = db.Column(db.String(50), unique=True)

    guitar_details = db.relationship('GuitarDetail', back_populates='product', uselist=False)
    accessory_details = db.relationship('AccessoryDetail', back_populates='product', uselist=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True) 

    cart_items = db.relationship('CartItem', back_populates='product')

    def __repr__(self):
        return f'<Product {self.name}>'


class GuitarDetail(db.Model):
    __tablename__ = 'guitardetails'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    strings_number = db.Column(db.Integer, nullable=False)
    body_material = db.Column(db.String(100), nullable=False)
    neck_material = db.Column(db.String(100), nullable=False)
    pickups = db.Column(db.String(255))

    product = db.relationship('Product', back_populates='guitar_details')

    def __repr__(self):
        return f'<GuitarDetail for Product {self.product_id}>'


class AccessoryDetail(db.Model):
    __tablename__ = 'accessorydetails'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    compatibility = db.Column(db.String(255))
    material = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)    

    product = db.relationship('Product', back_populates='accessory_details')

    def __repr__(self):
        return f'<AccessoryDetail for Product {self.product_id}>'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'shipped', 'cancelled', 'waiting_for_stock', name='order_status'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2))
    type = db.Column(db.Enum('regular', 'preorder', name='order_type'), nullable=False)
    expected_delivery_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'


class OrderItem(db.Model):
    __tablename__ = 'orderitems'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'
    

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')

    def __repr__(self):
        return f'<CartItem {self.id}: {self.product.name} x{self.quantity}>'