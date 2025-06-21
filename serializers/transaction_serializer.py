from marshmallow import Schema, fields

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    amount = fields.Float(required=True)
    description = fields.Str(allow_none=True)
    date = fields.DateTime(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)