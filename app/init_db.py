from app.default.models import User
from app import db


def init_db():
    db.create_all()
    u = User(username="admin", admin=True)
    if u.password_hash is None:
        u.set_password("password")
    db.session.add(u)
    db.session.commit()


if __name__ == "main":
    init_db()
