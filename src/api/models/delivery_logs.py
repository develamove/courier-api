from marshmallow import fields
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, func
from src.extensions import database, marshmallow


class DeliveryLogsModel(database.Model):
    __tablename__ = 't_delivery_logs'

    id = Column(Integer, primary_key=True)
    delivery_id = Column(Integer)
    name = Column(String(50))
    value = Column(String(1))
    retry = Column(Integer)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, delivery_id, name, value, retry):
        self.delivery_id = delivery_id
        self.name = name
        self.value = value
        self.retry = retry

    def __repr__(self):
        return '<DeliveryStatus %r>' % self.name


class DeliveryLogSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = DeliveryLogsModel
        strict = True

    id = fields.Int(dump_only=True)
    delivery_id = fields.Int(dump_only=True)
    name = fields.Str(missing='')
    retry = fields.Integer(missing=1)
    value = fields.Str(missing='')
    created_timestamp = fields.DateTime(dump_only=True)
