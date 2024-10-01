from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db  # Import db from __init__.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    active = db.Column(db.String(1), default='1')
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    dummy_column = db.Column(db.String(100))

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.String(1), default='1')

    # Relationship with Product model
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discounted_price = db.Column(db.Float)
    img_path = db.Column(db.String(255))
    description = db.Column(db.Text)
    active = db.Column(db.String(1), default='1')

    # Foreign key reference to Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    active = db.Column(db.String(1), default='1')
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    product = db.relationship('Product')

class ProductDetailImages(db.Model):
    __tablename__ = 'product_detail_images'
    id = db.Column(db.Integer, primary_key=True)    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    img_path = db.Column(db.String(255))
    active = db.Column(db.String(1), default='1')
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    review = db.Column(db.Text, nullable=False)
    active = db.Column(db.String(1), default='1')
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='reviews')
    product = db.relationship('Product', backref='reviews')

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Made nullable
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    active = db.Column(db.String(1), default='1')
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='contacts')  # 'contacts' used for clarity, can be None for unregistered users

      

