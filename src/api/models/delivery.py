from src.extensions import database, marshmallow
from sqlalchemy import Column, DateTime, Integer, String, func, Text
from marshmallow import fields


class DeliveryModel(database.Model):
    __tablename__ = 't_delivery'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    tracking_id = Column(String(40))
    receipt_id = Column(String(30))
    is_cod = Column(String(1), nullable=False)
    is_provincial = Column(String(1), nullable=False)
    is_for_pick_up = Column(String(1), nullable=False)
    is_already_pick_up = Column(String(1), nullable=False)
    is_in_transit = Column(String(1), nullable=False)
    is_remitted = Column(String(1), nullable=False)
    is_delivered = Column(String(1), nullable=False)
    is_successful = Column(String(1), nullable=False)
    is_cancelled = Column(String(1), nullable=False)
    retry = Column(Integer)
    item_name = Column(String(50))
    item_type = Column(String(5), nullable=False)
    item_amount = Column(Integer, nullable=False)
    item_weight = Column(Integer, nullable=False)
    total_amount = Column(Integer)
    comments = Column(Text(200))
    set_user = Column(String(20))
    set_timestamp = Column(DateTime, nullable=True)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, client_id, tracking_id, item_name, item_type, item_amount, is_cod, is_provincial, item_value=0,
                 item_weight=1, item_protection=0, total_amount=0, receipt_id='', is_for_pick_up='T',
                 is_already_pick_up='F', is_in_transit='F', is_remitted='F', is_delivered='F', is_successful='F',
                 is_cancelled='F', comments='', retry=1):
        self.tracking_id = tracking_id
        self.client_id = client_id
        self.receipt_id = receipt_id
        self.is_cod = is_cod
        self.is_provincial = is_provincial
        self.is_for_pick_up = is_for_pick_up
        self.is_already_pick_up = is_already_pick_up
        self.is_in_transit = is_in_transit
        self.is_remitted = is_remitted
        self.is_delivered = is_delivered
        self.is_successful = is_successful
        self.is_cancelled = is_cancelled
        self.retry = retry
        self.item_name = item_name
        self.item_type = item_type
        self.item_value = item_value
        self.item_protection = item_protection
        self.item_weight = item_weight
        self.item_amount = item_amount
        self.total_amount = total_amount
        self.comments = comments

    def __repr__(self):
        return '<DeliveryLogs %r>' % self.tracking_id


class DeliverySchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = DeliveryModel
        strict = True

    id = fields.Int(dump_only=True)
    client_id = fields.Int(dump_only=True)
    tracking_id = fields.Str(missing='')
    receipt_id = fields.Str(missing='')
    is_cod = fields.Str(missing='')
    is_provincial = fields.Str(missing='')
    is_for_pick_up = fields.Str(missing='')
    is_already_pick_up = fields.Str(missing='')
    is_remitted = fields.Str(missing='')
    is_delivered = fields.Str(missing='')
    is_successful = fields.Str(missing='')
    is_cancelled = fields.Str(missing='')
    item_name = fields.Str(missing='')
    item_type = fields.Str(missing='')
    item_value = fields.Int(missing=0)
    item_weight = fields.Int(missing=0)
    item_protection = fields.Int(missing=0)
    item_amount = fields.Int(missing=0)
    total_amount = fields.Int(missing=0)
    retry = fields.Int(missing=1)
    comments = fields.Str(missing='')
    set_user = fields.DateTime(dump_only=True)
    set_timestamp = fields.DateTime(dump_only=True)
    created_timestamp = fields.DateTime(dump_only=True)
