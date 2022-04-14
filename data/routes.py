import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin


class Route(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'route'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    route_name = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.Date)
    end_date = sqlalchemy.Column(sqlalchemy.Date)
    start_time = sqlalchemy.Column(sqlalchemy.Time)
    end_time = sqlalchemy.Column(sqlalchemy.Time)
    start_point = sqlalchemy.Column(sqlalchemy.String)
    end_point = sqlalchemy.Column(sqlalchemy.String)
    driver_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("drivers.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    bus_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("buses.id"))

    driver = orm.relation('Driver', back_populates='route')
    user_created = orm.relation('User', back_populates='route')
    bus = orm.relation('Bus', back_populates='route')

    def __init__(
            self, route_name=None,
            start_date=None, end_date=None, start_time=None, end_time=None,
            start_point=None, end_point=None,
            driver_id=None, user_id=None, bus_id=None
    ):
        self.route_name = route_name
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time

        self.start_point = start_point
        self.end_point = end_point

        self.driver_id = driver_id
        self.user_id = user_id
        self.bus_id = bus_id
