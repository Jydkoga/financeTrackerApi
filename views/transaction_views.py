from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.category import Category
from models.user import User
from serializers.transaction_serializer import transaction_schema, transactions_schema
from flask_cors import cross_origin

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/',methods=["GET"])
@cross_origin()
def get_transactions():
    try:
        transactions = Transaction.query.all()
        return jsonify(transactions_schema.dump(transactions)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@transaction_bp.route('/add', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        new_transaction = transaction_schema.load(data, session=db.session)
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(transaction_schema.dump(new_transaction)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400