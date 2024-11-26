# models.py
from datetime import datetime
from database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # 应存储哈希密码
    balance = db.Column(db.Float, default=0.0, nullable=False)

    transactions = db.relationship('Transaction', backref='user', lazy=True)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 取款、存款、转账等
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))  # 例如转账的对方账号
