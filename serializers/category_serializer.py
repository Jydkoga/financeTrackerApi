from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.category import Category
from marshmallow_sqlalchemy.fields import Nested
from serializers.transaction_serializer import TransactionSchema

class CategorySchema(SQLAlchemySchema):
    class Meta:
        model = Category
        load_instance = True

    id = auto_field()
    name = auto_field()
    transactions = Nested(TransactionSchema, many=True, exclude=('category',))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)