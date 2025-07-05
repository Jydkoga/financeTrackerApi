from flask import Blueprint, request, jsonify
from models import db
from models.transaction import Transaction
from models.transaction_group import TransactionGroup
from models.category import Category
from models.user import User
from serializers.category_serializer import category_schema, categories_schema
from flask_cors import cross_origin
from marshmallow import ValidationError

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=["GET"])
@cross_origin()
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify(categories_schema.dump(categories)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
      
@category_bp.route('/add', methods=['POST'])
@cross_origin()
def add_category():
    try:
        data = request.get_json()
        try:
            new_category = category_schema.load(data, session=db.session)
        except ValidationError as err:
            return jsonify({"error": "Validation error", "messages": err.messages}), 400
        #checking for uniqueness of category name
        existing_category = Category.query.filter_by(name=data.get('name')).first()
        if existing_category:
          return jsonify({"error": "Category with this name already exists."}), 400
        db.session.add(new_category)
        db.session.commit()
        return jsonify(category_schema.dump(new_category)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@cross_origin()
def delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found."}), 404

        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": f"Category '{category.name}' deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
