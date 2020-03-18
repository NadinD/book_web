import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase

roles_users = sqlalchemy.Table('roles_users', SqlAlchemyBase.metadata,
                               sqlalchemy.Column('user_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('users.id')),
                               sqlalchemy.Column('role_id', sqlalchemy.Integer(), sqlalchemy.ForeignKey('roles.id'))
                               )


class Roles(SqlAlchemyBase, UserMixin):
    __tablename__ = 'roles'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), unique=True)
    description = sqlalchemy.Column(sqlalchemy.String(255))

    def __repr__(self):
        return '<Role id: {}, name: {} >'.format(self.id, self.name)
