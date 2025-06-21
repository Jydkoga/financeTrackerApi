from models import db
from models.transaction import Transaction
from models.user import User


class TransactionGroup(db.Model):
    __tablename__ = 'transaction_groups'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)    
    transactions = db.relationship('Transaction', backref='transaction_group', lazy=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<TransactionGroup {self.id} - {self.title}>'