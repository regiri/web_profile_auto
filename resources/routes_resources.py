from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from datetime import date, time
from data.routes import Route


parser = reqparse.RequestParser()
parser.add_argument('route_name', required=True)
parser.add_argument('start_date', required=True, type=date)
parser.add_argument('end_date', required=True, type=date)
parser.add_argument('start_time', required=True, type=time)
parser.add_argument('end_time', required=True, type=time)
parser.add_argument('start_point', required=True)
parser.add_argument('end_point', required=True)
parser.add_argument('driver_id', required=True, type=int)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('bus_id', required=True, type=int)


def abort_if_route_not_found(route_id):
    db_sess = db_session.create_session()
    route = db_sess.query(Route).get(route_id)
    if not route:
        abort(404, message=f"Route {route_id} not found")


class RouteResource(Resource):
    def get(self, route_id):
        abort_if_route_not_found(route_id)
        db_sess = db_session.create_session()
        route = db_sess.query(Route).get(route_id)
        return jsonify({'route': route.to_dict(
            only=('route_name', 'start_date', 'end_date', 'start_time', 'end_time',
                  'start_point', 'end_point', 'driver_id', 'user_id', 'bus_id')
        )})

    def delete(self, route_id):
        abort_if_route_not_found(route_id)
        db_sess = db_session.create_session()
        route = db_sess.query(Route).get(route_id)
        db_sess.delete(route)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class RouteListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        routes = db_sess.query(Route).all()
        return jsonify({'route': [item.to_dict(
            only=('route_name', 'start_date', 'end_date', 'start_time', 'end_time',
                  'start_point', 'end_point', 'driver_id', 'user_id', 'bus_id')
        )] for item in routes})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        route = Route(
            route_name=args['route_name'],
            start_point=args['start_point'],
            end_point=args['end_point'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            start_time=args['start_time'],
            end_time=args['end_time'],
            driver_id=args['driver_id'],
            bus_id=args['bus_id'],
            user_id=args['user_id']
        )
        db_sess.add(route)
        db_sess.commit()
        return jsonify({'success': 'OK'})