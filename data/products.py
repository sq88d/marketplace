import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String,
                                nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String,
                              unique=True, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
