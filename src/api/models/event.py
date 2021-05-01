from marshmallow import fields
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Text, func
from src.extensions import database, marshmallow


class EventModel(database.Model):
    __tablename__ = 't_event'

    id = Column(Integer, primary_key=True)
    delivery_id = database.Column(Integer, ForeignKey('t_delivery.id'))
    name = Column(String(50))
    remarks = Column(Text(200))
    updated_timestamp = Column(DateTime, nullable=True)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, delivery_id, name, remarks, **kwargs):
        super(EventModel, self).__init__(**kwargs)
        self.delivery_id = delivery_id
        self.name = name
        self.remarks = remarks

    def __repr__(self):
        return '<Event %r>' % self.name


class EventSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = EventModel
        strict = True

    id = fields.Int(dump_only=True)
    delivery_id = fields.Int(dump_only=True)
    name = fields.Str(missing='')
    remarks = fields.Str(missing='')
    created_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
    updated_timestamp = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S%z')
