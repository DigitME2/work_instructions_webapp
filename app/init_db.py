from app.default.models import User
from app.extensions import db


def init_db():
    db.create_all()
    if len(User.query.all()) == 0:
        u = User(username="admin", admin=True)
        if u.password_hash is None:
            u.set_password("digitme2")
        db.session.add(u)
        db.session.commit()


if __name__ == "main":
    init_db()
