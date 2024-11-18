from flask import Flask, jsonify, request
from database import init_db
from models import db
from services import handle_withdraw, handle_deposit, handle_balance

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/atm_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
init_db(app)

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    response = handle_withdraw(data['account_id'], data['amount'])
    return jsonify(response)

@app.route('/api/deposit', methods=['POST'])
def deposit():
    data = request.json
    response = handle_deposit(data['account_id'], data['amount'])
    return jsonify(response)

@app.route('/api/balance/<int:account_id>', methods=['GET'])
def balance(account_id):
    response = handle_balance(account_id)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
