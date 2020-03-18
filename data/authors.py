import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Authors(SqlAlchemyBase, UserMixin):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    middlename = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)
    books = orm.relation("Books", back_populates='author')

    def __repr__(self):
        return (self.name + ' ' + self.middlename + ' ' + self.surname)
