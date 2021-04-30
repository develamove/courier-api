from marshmallow import fields
from sqlalchemy import Column, DateTime, Integer, String, func, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.api.models.sender import SenderSchema
from src.api.models.recipient import RecipientSchema
from src.api.models.event import EventSchema
from src.extensions import database, marshmallow


class DeliveryModel(database.Model):
    __tablename__ = 't_delivery'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    tracking_number = Column(String(20))
    receipt_id = Column(String(30))
    item_description = Column(String(50))
    item_type = Column(String(5), nullable=False)
    item_value = Column(Integer, nullable=False)
    shipping_fee = Column(Integer, nullable=False)
    insurance_fee = Column(Integer, nullable=False)
    payment_method = Column(String(10), nullable=False)
    failure_reason = Column(Text(200))
    service_fees_payor = Column(String(30), nullable=False)
    cancellation_reason = Column(Text(200))
    transaction_total = Column(Integer)
    total = Column(Integer)
    remarks = Column(Text(200))
    status = Column(String(20))
    updated_timestamp = Column(DateTime, nullable=True)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    sender = relationship('SenderModel', uselist=False, lazy=True)
    recipient = relationship('RecipientModel', uselist=False, lazy=True)
    events = relationship('EventModel', backref='t_delivery', lazy=True)

    def __init__(self, client_id, tracking_number, item_description, item_type, item_value, shipping_fee,
                 payment_method, total, status, transaction_total, service_fees_payor, receipt_id='',
                 insurance_fee=0, **kwargs):
        super(DeliveryModel, self).__init__(**kwargs)
        self.client_id = client_id
        self.tracking_number = tracking_number
        self.receipt_id = receipt_id
        self.item_description = item_description
        self.service_fees_payor = service_fees_payor
        self.item_type = item_type
        self.item_value = item_value
        self.shipping_fee = shipping_fee
        self.payment_method = payment_method
        self.transaction_total = transaction_total
        self.total = total
        self.status = status
        self.insurance_fee = insurance_fee

    def __repr__(self):
        return '<Delivery %r>' % self.tracking_number


class DeliverySchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = DeliveryModel
        strict = True

    id = fields.Int(dump_only=True)
    client_id = fields.Int(dump_only=True)
    tracking_number = fields.Str(missing='')
    receipt_id = fields.Str(missing='')
    item_description = fields.Str(missing='')
    item_type = fields.Str(missing='')
    item_value = fields.Int(missing=0)
    shipping_fee = fields.Int(dump_only=True)
    insurance_fee = fields.Int(dump_only=True)
    transaction_total = fields.Int(missing=0)
    total = fields.Int(missing=0)
    payment_method = fields.Str(missing='')
    failure_reason = fields.Str(missing='')
    service_fees_payor = fields.Str(missing='')
    cancellation_reason = fields.Str(missing='')
    status = fields.Str(missing='')
    remarks = fields.Str(missing='')
    updated_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
    created_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
    sender = fields.Nested(SenderSchema)
    recipient = fields.Nested(RecipientSchema)
    events = fields.Nested(EventSchema, many=True)
