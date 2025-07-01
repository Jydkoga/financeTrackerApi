from models import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    transaction_group_id = db.Column(db.Integer, db.ForeignKey('transaction_groups.id'), nullable=True)

    def __repr__(self):
        return f'<Transaction {self.id} - {self.amount}>'