from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.transaction_group import TransactionGroup
from marshmallow_sqlalchemy.fields import Nested
from serializers.transaction_serializer import TransactionSchema


class TransactionGroupSchema(SQLAlchemySchema):
    class Meta:
        model = TransactionGroup
        load_instance = True
        include_fk = True

    id = auto_field(dump_only=True)
    title = auto_field(required=True)
    description = auto_field(allow_none=True)
    user_id = auto_field(required=True)
    date_created = auto_field(dump_only=True)
    transactions = Nested(TransactionSchema, many=True, dump_only=True)
    total = auto_field(dump_only=True)


transaction_group_schema = TransactionGroupSchema()
transaction_groups_schema = TransactionGroupSchema(many=True)
