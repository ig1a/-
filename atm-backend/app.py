# app.py
from flask import Flask, request, jsonify, session
from database import init_db
from models import User
from services import ATMService
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # 用于会话管理

init_db(app)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    card_number = data.get('card_number')
    password = data.get('password')
    initial_deposit = data.get('initial_deposit', 0.0)

    if User.query.filter_by(card_number=card_number).first():
        return jsonify({'message': '卡号已存在'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(card_number=card_number, password=hashed_password, balance=initial_deposit)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    card_number = data.get('card_number')
    password = data.get('password')

    user = ATMService.authenticate(card_number, password)
    if user:
        session['user_id'] = user.id
        return jsonify({'message': '登录成功'}), 200
    else:
        return jsonify({'message': '认证失败'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': '已登出'}), 200


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': '未登录'}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    data = request.json
    amount = data.get('amount')
    if amount <= 0:
        return jsonify({'message': '取款金额必须大于0'}), 400
    user = User.query.get(session['user_id'])
    success, message = ATMService.withdraw(user, amount)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400


@app.route('/deposit', methods=['POST'])
@login_required
def deposit():
    data = request.json
    amount = data.get('amount')
    if amount <= 0:
        return jsonify({'message': '存款金额必须大于0'}), 400
    user = User.query.get(session['user_id'])
    success, message = ATMService.deposit(user, amount)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.json
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    if new_password != confirm_password:
        return jsonify({'message': '两次输入的密码不一致'}), 400
    user = User.query.get(session['user_id'])
    success, message = ATMService.change_password(user, new_password)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400


@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.json
    recipient_card = data.get('recipient_card')
    amount = data.get('amount')
    if amount <= 0:
        return jsonify({'message': '转账金额必须大于0'}), 400
    user = User.query.get(session['user_id'])
    success, message = ATMService.transfer(user, recipient_card, amount)
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'message': message}), 400


@app.route('/balance', methods=['GET'])
@login_required
def balance():
    user = User.query.get(session['user_id'])
    current_balance = ATMService.get_balance(user)
    return jsonify({'balance': current_balance}), 200


@app.route('/transactions', methods=['GET'])
@login_required
def transactions():
    user = User.query.get(session['user_id'])
    trans = ATMService.get_transactions(user)
    transactions_list = [{
        'type': t.type,
        'amount': t.amount,
        'timestamp': t.timestamp,
        'description': t.description
    } for t in trans]
    return jsonify({'transactions': transactions_list}), 200


@app.route('/print_receipt/<int:transaction_id>', methods=['GET'])
@login_required
def print_receipt(transaction_id):
    user = User.query.get(session['user_id'])
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user.id).first()
    if not transaction:
        return jsonify({'message': '交易记录不存在'}), 404
    receipt = ATMService.print_receipt(transaction)
    return jsonify({'receipt': receipt}), 200


if __name__ == '__main__':
    app.run(debug=True)
