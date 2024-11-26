# services.py
from models import User, Transaction
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class ATMService:
    @staticmethod
    def authenticate(card_number, password):
        user = User.query.filter_by(card_number=card_number).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def withdraw(user, amount):
        if user.balance < amount:
            return False, "余额不足，无法完成取款"
        user.balance -= amount
        transaction = Transaction(user_id=user.id, type='取款', amount=amount)
        db.session.add(transaction)
        db.session.commit()
        return True, "取款成功"

    @staticmethod
    def deposit(user, amount):
        user.balance += amount
        transaction = Transaction(user_id=user.id, type='存款', amount=amount)
        db.session.add(transaction)
        db.session.commit()
        return True, "存款成功"

    @staticmethod
    def change_password(user, new_password):
        user.password = generate_password_hash(new_password)
        transaction = Transaction(user_id=user.id, type='修改密码', amount=0)
        db.session.add(transaction)
        db.session.commit()
        return True, "密码修改成功"

    @staticmethod
    def transfer(user, recipient_card, amount):
        if user.balance < amount:
            return False, "余额不足，无法完成转账"
        recipient = User.query.filter_by(card_number=recipient_card).first()
        if not recipient:
            return False, "收款人账号不存在"
        user.balance -= amount
        recipient.balance += amount
        transaction_out = Transaction(user_id=user.id, type='转账出', amount=amount, description=f"转给 {recipient_card}")
        transaction_in = Transaction(user_id=recipient.id, type='转账入', amount=amount, description=f"来自 {user.card_number}")
        db.session.add_all([transaction_out, transaction_in])
        db.session.commit()
        return True, "转账成功"

    @staticmethod
    def get_balance(user):
        return user.balance

    @staticmethod
    def get_transactions(user, limit=10):
        return Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).limit(limit).all()

    @staticmethod
    def print_receipt(transaction):
        # 模拟打印凭条，可以根据需要调整
        receipt = f"""
        交易类型: {transaction.type}
        金额: {transaction.amount}
        时间: {transaction.timestamp}
        """
        if transaction.description:
            receipt += f"描述: {transaction.description}\n"
        return receipt
