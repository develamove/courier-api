from src.extensions import database, marshmallow
from sqlalchemy import Column, DateTime, Integer, String, func


class ProvinceModel(database.Model):
    __tablename__ = 't_province'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    is_pickup_available = Column(String(1))
    # kind = Column(String(50))
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, name, is_pickup_available):
        self.name = name
        self.is_pickup_available = is_pickup_available

    def __repr__(self):
        return '<Province %r>' % self.name


class ProvinceSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = ProvinceModel
        strict = True
