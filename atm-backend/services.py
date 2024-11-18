from models import db, Account, Transaction


#该文件用于处理实际业务逻辑，目前只能实现基本功能

def handle_withdraw(account_id, amount):
    account = Account.query.get(account_id)
    if not account:
        return {"status": "error", "message": "Account not found"}

    if account.balance < amount:
        return {"status": "error", "message": "Insufficient balance"}

    account.balance -= amount
    transaction = Transaction(account_id=account_id, type='withdraw', amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return {"status": "success", "balance": float(account.balance)}


def handle_deposit(account_id, amount):
    account = Account.query.get(account_id)
    if not account:
        return {"status": "error", "message": "Account not found"}

    account.balance += amount
    transaction = Transaction(account_id=account_id, type='deposit', amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return {"status": "success", "balance": float(account.balance)}


def handle_balance(account_id):
    account = Account.query.get(account_id)
    if not account:
        return {"status": "error", "message": "Account not found"}
    return {"status": "success", "balance": float(account.balance)}
