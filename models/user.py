from models import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    total_balance = db.Column(db.Float, default=0.0)

    transactions = db.relationship("Transaction", backref="user", lazy=True)
    transaction_groups = db.relationship("TransactionGroup", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.id} - {self.username}>"

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, attempted_password):
        return check_password_hash(self.password_hash, attempted_password)

    def __init__(self, username, total_balance=0.0, password=None):
        self.username = username
        self.total_balance = total_balance
        if password:
            self.set_password(password)
