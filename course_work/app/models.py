from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from datetime import datetime
from werkzeug.security import check_password_hash

from .extension import db


class User(db.Model, UserMixin):
    __tablename__ ='Users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False) 
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.login}>'


class Brand(db.Model):
    __tablename__ = 'Brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', backref='brand', lazy=True)

    def __repr__(self):
        return f'<Brand {self.name}>'


class Category(db.Model):
    __tablename__ = 'Categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('Brands.id'))
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    guitar_details = db.relationship('GuitarDetail', back_populates='product', uselist=False)
    accessory_details = db.relationship('AccessoryDetail', back_populates='product', uselist=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    ratings = db.relationship('Rating', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'


class GuitarDetail(db.Model):
    __tablename__ = 'GuitarDetails'

    product_id = db.Column(db.Integer, db.ForeignKey('Products.id', ondelete='CASCADE'), primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    strings_number = db.Column(db.Integer, nullable=False)
    body_material = db.Column(db.String(100), nullable=False)
    neck_material = db.Column(db.String(100), nullable=False)
    pickups = db.Column(db.String(255))

    product = db.relationship('Product', back_populates='guitar_details')

    def __repr__(self):
        return f'<GuitarDetail for Product {self.product_id}>'


class AccessoryDetail(db.Model):
    __tablename__ = 'AccessoryDetails'

    product_id = db.Column(db.Integer, db.ForeignKey('Products.id', ondelete='CASCADE'), primary_key=True)
    compatibility = db.Column(db.String(255))
    material = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)    

    product = db.relationship('Product', back_populates='accessory_details')

    def __repr__(self):
        return f'<AccessoryDetail for Product {self.product_id}>'


class Order(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'paid', 'shipped', 'cancelled', 'waiting_for_stock', name='order_status'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2))
    type = db.Column(db.Enum('regular', 'preorder', name='order_type'), nullable=False)
    expected_delivery_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'


class OrderItem(db.Model):
    __tablename__ = 'OrderItems'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'


class Rating(db.Model):
    __tablename__ = 'Ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_rating'),
    )

    def __repr__(self):
        return f'<Rating {self.stars} stars by User {self.user_id} for Product {self.product_id}>'