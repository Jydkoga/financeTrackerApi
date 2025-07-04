
from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.transaction_group import TransactionGroup
from models.category import Category
from models.user import User
from serializers.transaction_serializer import transaction_schema, transactions_schema
from flask_cors import cross_origin

from marshmallow import ValidationError

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/',methods=["GET"])
@cross_origin()
def get_transactions():
    try:
        user_id = request.args.get('user_id', type=int)
        if user_id is None:
            return jsonify({"error": "Missing user_id in query parameters"}), 400
            
        transactions = Transaction.query.filter_by(user_id=user_id, is_deleted=False).all()
        return jsonify(transactions_schema.dump(transactions)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@transaction_bp.route('/add', methods=['POST'])
@cross_origin()
def add_transaction():
    try:
        data = request.get_json()
        print("Received data:", data)
        try:   
            new_transaction = transaction_schema.load(data, session=db.session)
        except ValidationError as err:
            print("Validation error:", err.messages)
            return jsonify({"error": "Validation error", "messages": err.messages}), 400
        print("Transaction fields:", new_transaction.title, new_transaction.description,
      new_transaction.amount, new_transaction.user_id, new_transaction.transaction_group_id)
        
        db.session.add(new_transaction)
        db.session.flush()
        
        transaction_group = db.session.get(TransactionGroup, new_transaction.transaction_group_id)
        user = db.session.get(User, new_transaction.user_id)
        
        # Add transaction amount to the transaction group total
        if transaction_group:
            transaction_group.total += new_transaction.amount

        # Update the user's total balance
        if user:
            user.total_balance += new_transaction.amount
        return jsonify(transaction_schema.dump(new_transaction)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@transaction_bp.route('/<int:transaction_id>/remove', methods=['DELETE'])
@cross_origin()
def remove_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        # Update the transaction group total and user balance before deletion
        transaction_group = db.session.get(TransactionGroup, transaction.transaction_group_id)
        user = db.session.get(User, transaction.user_id)
        
        if transaction_group:
            transaction_group.total -= transaction.amount
        
        if user:
            user.total_balance -= transaction.amount
        
        db.session.delete(transaction)
        db.session.commit()
        
        return jsonify({"message": "Transaction removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400