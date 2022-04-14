import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin


class Bus(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'buses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    brand = sqlalchemy.Column(sqlalchemy.String)
    last_maintenance = sqlalchemy.Column(sqlalchemy.Date)
    next_maintenance = sqlalchemy.Column(sqlalchemy.Date)
    seats_number = sqlalchemy.Column(sqlalchemy.Integer)
    about = sqlalchemy.Column(sqlalchemy.String)

    route = orm.relation('Route')

    def __init__(
            self, number, brand=None, last_maintenance=None, next_maintenance=None, seats_number=None, about=None
    ):
        self.number = number
        self.brand = brand
        self.last_maintenance = last_maintenance
        self.next_maintenance = next_maintenance
        self.seats_number = seats_number
        self.about = about

    def __str__(self):
        return f'{self.number} {self.brand}'
