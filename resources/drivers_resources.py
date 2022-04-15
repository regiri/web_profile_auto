from flask_restful import reqparse, abort, Resource
from flask import jsonify
from data import db_session
from data.drivers import Driver


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('lastname', required=True)
parser.add_argument('phone_number', required=True)


def abort_if_driver_not_found(driver_id):
    db_sess = db_session.create_session()
    driver = db_sess.query(Driver).get(driver_id)
    if not driver:
        abort(404, message=f"Driver {driver_id} not found")


class DriverResource(Resource):
    def get(self, driver_id):
        abort_if_driver_not_found(driver_id)
        db_sess = db_session.create_session()
        driver = db_sess.query(Driver).get(driver_id)
        return jsonify({'driver': driver.to_dict(
            only=('name', 'surname', 'lastname', 'phone_number')
        )})

    def delete(self, driver_id):
        abort_if_driver_not_found(driver_id)
        db_sess = db_session.create_session()
        driver = db_sess.query(Driver).get(driver_id)
        db_sess.delete(driver)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class DriversListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        drivers = db_sess.query(Driver).all()
        return jsonify({'driver': [item.to_dict(
            only=('name', 'surname', 'lastname', 'phone_number')
        )] for item in drivers})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        driver = Driver(
            name=args['name'],
            surname=args['surname'],
            lastname=args['lastname'],
            phone_number=args['phone_number']
        )
        db_sess.add(driver)
        db_sess.commit()
        return jsonify({'success': 'OK'})
