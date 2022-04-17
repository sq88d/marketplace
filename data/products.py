import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String,
                              nullable=True)

