from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)  # bcrypt hash

    @staticmethod
    def hash_password(plain: str) -> bytes:
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, plain: str) -> bool:
        try:
            return bcrypt.checkpw(plain.encode("utf-8"), self.password_hash)
        except Exception:
            return False
