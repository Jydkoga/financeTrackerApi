from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.transaction_group import TransactionGroup
from models.category import Category
from models.user import User
from serializers.category_serializer import category_schema, categories_schema
from flask_cors import cross_origin
from marshmallow import ValidationError
import traceback
from sqlalchemy import func

category_bp = Blueprint("category", __name__)


@category_bp.route("/", methods=["GET"])
@cross_origin()
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify(categories_schema.dump(categories)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@category_bp.route("/add", methods=["POST"])
@cross_origin()
def add_category():
    try:
        data = request.get_json()
        # Normalize category name by stripping whitespace
        data["name"] = data["name"].strip()
        try:
            new_category = category_schema.load(data, session=db.session)
        except ValidationError as err:
            print("Validation error:", err.messages)
            return jsonify({"error": "Validation error", "messages": err.messages}), 400
        # checking for uniqueness of category name (case-insensitive, per user)
        existing_category = Category.query.filter(
            func.lower(Category.name) == data.get("name").lower(),
            Category.user_id == data.get("user_id"),
        ).first()
        if existing_category:
            print("Category with this name already exists:", existing_category.name)
            return jsonify({"error": "Category with this name already exists."}), 400
        db.session.add(new_category)
        db.session.commit()
        return jsonify(category_schema.dump(new_category)), 201
    except Exception as e:
        db.session.rollback()
        print("Error during commit:", str(e))
        return jsonify({"error": str(e)}), 400


@category_bp.route("/user/<int:user_id>", methods=["GET"])
@cross_origin()
def get_user_categories(user_id):
    print("i got here")
    try:
        print("Fetching categories for user_id:", user_id)
        print("User.query.all():", User.query.all())
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404

        categories = Category.query.filter_by(user_id=user_id).all()
        print("Categories found:", categories)
        return jsonify(categories_schema.dump(categories)), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@category_bp.route("/delete/<int:category_id>", methods=["DELETE"])
@cross_origin()
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found."}), 404

        db.session.delete(category)
        db.session.commit()
        return (
            jsonify({"message": f"Category '{category.name}' deleted successfully."}),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
