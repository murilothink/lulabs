from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    orders = db.relationship("Order", backref="user", lazy=True)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    date = db.Column(db.String, nullable=False)
    total = db.Column(db.Float, nullable=False)
    products = db.relationship("Product", backref="order", lazy=True)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
