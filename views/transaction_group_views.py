from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.transaction_group import TransactionGroup
from models.category import Category
from models.user import User
from serializers.transaction_group_serializer import (
    transaction_group_schema,
    transaction_groups_schema,
)
from flask_cors import cross_origin
from marshmallow.exceptions import ValidationError

transaction_group_bp = Blueprint("transaction_group", __name__)


@transaction_group_bp.route("/", methods=["GET"])
@cross_origin()
def get_transaction_groups():
    try:
        transaction_groups = TransactionGroup.query.all()
        return jsonify(transaction_groups_schema.dump(transaction_groups)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@transaction_group_bp.route("/add", methods=["POST"])
@cross_origin()
def add_transaction_group():
    try:
        data = request.get_json()
        print("Received data for new transaction group:", data)
        user = User.query.get(data.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 404
        try:
            new_transaction_group = transaction_group_schema.load(
                data, session=db.session
            )
        except ValidationError as err:
            print("Validation error:", err.messages)
            return jsonify({"error": err.messages}), 400
        # new_transaction_group = transaction_group_schema.load(data, session=db.session)
        print("Loaded new transaction group:", new_transaction_group)
        db.session.add(new_transaction_group)
        db.session.commit()
        print(
            "Committed transaction group:",
            transaction_group_schema.dump(new_transaction_group),
        )
        return jsonify(transaction_group_schema.dump(new_transaction_group)), 201
    except Exception as e:
        db.session.rollback()
        print("Error during commit:", str(e))
        return jsonify({"error": str(e)}), 400


@transaction_group_bp.route("/<int:group_id>", methods=["GET"])
@cross_origin()
def get_transaction_group(group_id):
    try:
        transaction_group = TransactionGroup.query.get_or_404(group_id)
        return jsonify(transaction_group_schema.dump(transaction_group)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
