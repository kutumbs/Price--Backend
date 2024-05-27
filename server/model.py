# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates

# metadata = MetaData()
# db = SQLAlchemy(metadata=metadata)

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     products = db.relationship('Product', backref='user', lazy=True, cascade="all, delete-orphan")

#     @validates('password')
#     def validate_password(self, key, password):
#         if len(password) < 8:
#             raise ValueError('Password must be more than 8 characters.')
#         return password

#     @validates('email')
#     def validate_email(self, key, email):
#         if not email.endswith("@gmail.com"):
#             raise ValueError("Email is not valid. It should end with @gmail.com")
#         return email

# class Product(db.Model, SerializerMixin):
#     __tablename__ = 'products'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.String, nullable=False)
#     rating = db.Column(db.String)
#     image_url = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     stores = db.relationship('Store', secondary='productstores', backref=db.backref('products', lazy='dynamic'))

# class Store(db.Model, SerializerMixin):
#     __tablename__ = 'stores'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     rating = db.Column(db.Integer)
#     product_stores = db.relationship('ProductStore', backref='stores', overlaps='products,productstores')

# class ProductStore(db.Model, SerializerMixin):
#     __tablename__ = 'productstores'
#     id = db.Column(db.Integer, primary_key=True)
#     store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     store = db.relationship('Store', backref='productstores', overlaps='productstores,products')
#     product = db.relationship('Product', backref='stores', overlaps='stores,productstores')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pricehunter_database_lsxq_user:f1UieqGJndcgiAEi3oyv14BywSrgtKU1@dpg-cp5kqlol5elc73e5uj40-a.oregon-postgres.render.com/pricehunter_database_lsxq'  # Adjust as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData()
db = SQLAlchemy(app, metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(280), nullable=False)
    products = db.relationship('Product', backref='user', lazy=True, cascade="all, delete-orphan")

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError('Password must be more than 8 characters.')
        return password

    @validates('email')
    def validate_email(self, key, email):
        if not email.endswith("@gmail.com"):
            raise ValueError("Email is not valid. It should end with @gmail.com")
        return email

    # @staticmethod
    # def extract_numeric_price(price_str):
    #     if not price_str:  # Check if the input string is None or empty
    #         return None
    #     # Remove any non-numeric characters, except for '.' (decimal separator)
    #     numeric_price = re.sub(r'[^0-9.]', '', price_str)
    #     if numeric_price:
    #         return float(numeric_price)
    #     return None

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String, nullable=False)
    rating = db.Column(db.String)
    image_url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_link = db.Column(db.String(500))
    product_stores = db.relationship('ProductStore', backref='product', lazy='dynamic')

class Store(db.Model, SerializerMixin):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer)
    product_stores = db.relationship('ProductStore', backref='store', lazy='dynamic')

class ProductStore(db.Model, SerializerMixin):
    __tablename__ = 'productstores'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(200))
    rating = db.Column(db.String)
    __table_args__ = (
        db.UniqueConstraint('product_id', 'store_id', name='unique_product_store'),
    )

    @validates('price')
    def validate_price(self, key, price):
        # Ensure the price is properly formatted as a float
        if isinstance(price, str):
            price = User.extract_numeric_price(price)
        if price is None:
            raise ValueError('Invalid price format')
        return price

# Create the database and tables
with app.app_context():
    db.create_all()
