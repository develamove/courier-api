from sqlalchemy import Column, DateTime, Integer, String, func
from src.extensions import database, marshmallow


class ProvinceModel(database.Model):
    __tablename__ = 't_province'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    is_pickup_available = Column(String(1))
    created_timestamp = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, name, is_pickup_available, **kwargs):
        super(ProvinceModel, self).__init__(**kwargs)
        self.name = name
        self.is_pickup_available = is_pickup_available

    def __repr__(self):
        return '<Province %r>' % self.name


class ProvinceSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = ProvinceModel
        strict = True
