from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from datetime import date
from data.buses import Bus


parser = reqparse.RequestParser()
parser.add_argument('number', required=True)
parser.add_argument('brand', required=True)
parser.add_argument('last_maintenance', required=True, type=date)
parser.add_argument('next_maintenance', required=True, type=date)
parser.add_argument('seats_number', required=True, type=int)
parser.add_argument('about', required=True)


def abort_if_bus_not_found(bus_id):
    db_sess = db_session.create_session()
    bus = db_sess.query(Bus).get(bus_id)
    if not bus:
        abort(404, message=f"Bus {bus_id} not found")


class BusResource(Resource):
    def get(self, bus_id):
        abort_if_bus_not_found(bus_id)
        db_sess = db_session.create_session()
        bus = db_sess.query(Bus).get(bus_id)
        return jsonify({'bus': bus.to_dict(
            only=('number', 'brand', 'last_maintenance', 'next_maintenance', 'seats_number', 'about')
        )})

    def delete(self, bus_id):
        abort_if_bus_not_found(bus_id)
        db_sess = db_session.create_session()
        bus = db_sess.query(Bus).get(bus_id)
        db_sess.delete(bus)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class BusListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        buses = db_sess.query(Bus).all()
        return jsonify({'bus': [item.to_dict(
            only=('number', 'brand', 'last_maintenance', 'next_maintenance', 'seats_number', 'about')
        ) for item in buses]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        bus = Bus(
            number=args['number'],
            brand=args['brand'],
            last_maintenance=args['last_maintenance'],
            next_maintenance=args['next_maintenance'],
            seats_number=args['seats_number'],
            about=args['about']
        )
        db_sess.add(bus)
        db_sess.commit()
        return jsonify({'success': 'OK'})
