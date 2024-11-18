from models import db


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # 这应该能创建表结构
