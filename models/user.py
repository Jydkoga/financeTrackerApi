from models import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    total_balance = db.Column(db.Float, default=0.0)
    
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    transaction_groups = db.relationship('TransactionGroup', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'