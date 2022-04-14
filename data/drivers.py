import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin


class Driver(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'drivers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lastname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.String)

    route = orm.relation('Route')

    def __init__(
            self, name=None, surname=None, lastname=None, phone_number=None
    ):
        self.name = name
        self.surname = surname
        self.lastname = lastname
        self.phone_number = phone_number

    def __str__(self):
        return f'{self.surname} {self.name}'
