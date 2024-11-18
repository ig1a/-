from flask import Flask, jsonify, request
from database import init_db
from services import withdraw, deposit

app = Flask(__name__)
init_db(app)


#这是程序入口，先用flask试试（相互适合这个体积的小项目）

# 取款
@app.route('/api/withdraw', methods=['POST'])
def handle_withdraw():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    response = withdraw(account_id, amount)
    return jsonify(response)


# 存款
@app.route('/api/deposit', methods=['POST'])
def handle_deposit():
    data = request.json
    account_id = data['account_id']
    amount = data['amount']
    response = deposit(account_id, amount)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
