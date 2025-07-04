from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.transaction_group import TransactionGroup
from models.category import Category
from models.user import User
from serializers.transaction_group_serializer import transaction_group_schema, transaction_groups_schema
from flask_cors import cross_origin

transaction_group_bp = Blueprint('transaction_group', __name__)

@transaction_group_bp.route('/',methods=["GET"])
@cross_origin()
def get_transaction_groups():
    try:
        transaction_groups = TransactionGroup.query.all()
        return jsonify(transaction_groups_schema.dump(transaction_groups)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@transaction_group_bp.route('/add', methods=['POST'])
@cross_origin()
def add_transaction_group():
    try:
        data = request.get_json()
        new_transaction_group = transaction_group_schema.load(data, session=db.session)
        db.session.add(new_transaction_group)
        db.session.commit()
        return jsonify(transaction_group_schema.dump(new_transaction_group)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    

@transaction_group_bp.route('/<int:group_id>', methods=['GET'])
@cross_origin()
def get_transaction_group(group_id):
    try:
        transaction_group = TransactionGroup.query.get_or_404(group_id)
        return jsonify(transaction_group_schema.dump(transaction_group)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
