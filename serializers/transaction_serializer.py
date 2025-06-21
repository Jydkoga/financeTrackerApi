from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models.transaction import Transaction

class TransactionSchema(SQLAlchemySchema):
    class Meta:
        model = Transaction
        load_instance = True

    id = auto_field(dump_only=True)
    title = auto_field(required=True)
    amount = auto_field(required=True)
    description = auto_field(allow_none=True)
    date = auto_field(required=True)
    user_id = auto_field(required=True)
    category_id = auto_field(required=True)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)