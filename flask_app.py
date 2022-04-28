from flask import Flask, render_template, redirect, make_response, jsonify, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from resources import drivers_resources, buses_resources, routes_resources
from data import db_session
from data.users import User
from data.buses import Bus
from data.drivers import Driver
from data.routes import Route
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.addbusform import BusForm
from forms.adddriverform import DriverForm
from forms.addrouteform import RouteForm


fapp = Flask(__name__)
api = Api(fapp)
fapp.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(fapp)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@fapp.route('/', methods=['GET', 'POST'])
@fapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/all_routes')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@fapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@fapp.errorhandler(404)
def not_found(error):
    return make_response(jsonify(({'error': 'Not found'})), 404)


@fapp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message='Пароли не совпадают'
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message='Такой пользователь уже есть'
            )
        user = User(
            form.email.data,
            form.password.data,
            name=form.name.data,
            surname=form.surname.data,
            access_level=form.access_level.data
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@login_required
@fapp.route('/all_routes')
def all_routes():
    db_sess = db_session.create_session()
    routes = db_sess.query(Route).all()
    return render_template('all_routes.html', routes=routes, title='Список рейсов')


@login_required
@fapp.route('/add_route', methods=['GET', 'POST'])
def add_route():
    form = RouteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        route = Route(
            route_name=form.route_name.data,
            start_point=form.start_point.data,
            end_point=form.end_point.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            driver_id=form.driver.data.id,
            bus_id=form.bus.data.id,
            user_id=current_user.id
        )
        db_sess.add(route)
        db_sess.commit()
        return redirect('/all_routes')
    return render_template('route.html', form=form, title='Добавление маршрута')


@login_required
@fapp.route('/edit_route/<int:route_id>', methods=['GET', 'POST'])
def edit_route(route_id):
    form = RouteForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        route = db_sess.query(Route).filter(Route.id == route_id).first()
        if route:
            form.route_name.data = route.route_name
            form.start_point.data = route.start_point
            form.end_point.data = route.end_point
            form.start_date.data = route.start_date
            form.end_date.data = route.end_date
            form.start_time.data = route.start_time
            form.end_time.data = route.end_time
            form.driver.data = route.driver
            form.bus.data = route.bus
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        route = db_sess.query(Route).filter(Route.id == route_id).first()
        if route:
            route.route_name = form.route_name.data
            route.start_point = form.start_point.data
            route.end_point = form.end_point.data
            route.start_date = form.start_date.data
            route.end_date = form.end_date.data
            route.start_time = form.start_time.data
            route.end_time = form.end_time.data
            route.driver_id = form.driver.id
            route.bus_id = form.bus.id
            route.user_id = current_user.id
            db_sess.commit()
            return redirect('/all_routes')
        else:
            abort(404)
    return render_template('route.html', form=form, title='Редактирование маршрута')


@login_required
@fapp.route('/delete_route/<int:route_id>', methods=['GET', 'POST'])
def delete_route(route_id):
    db_sess = db_session.create_session()
    route = db_sess.query(Route).filter(Route.id == route_id).first()
    if route:
        db_sess.delete(route)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/all_routes')


@login_required
@fapp.route('/all_buses')
def all_buses():
    db_sess = db_session.create_session()
    buses = db_sess.query(Bus).all()
    return render_template('all_buses.html', buses=buses, title='Список автобусов')


@login_required
@fapp.route('/add_bus', methods=['GET', 'POST'])
def add_bus():
    form = BusForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        bus = Bus(
            number=form.number.data,
            brand=form.brand.data,
            last_maintenance=form.last_maintenance.data,
            next_maintenance=form.next_maintenance.data,
            seats_number=form.seats_number.data,
            about=form.about.data
        )
        db_sess.add(bus)
        db_sess.commit()
        return redirect('/all_buses')
    return render_template('bus.html', form=form, title='Добавление автобуса')


@login_required
@fapp.route('/edit_bus/<int:bus_id>', methods=['GET', 'POST'])
def edit_bus(bus_id):
    form = BusForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        bus = db_sess.query(Bus).filter(Bus.id == bus_id).first()
        if bus:
            form.number.data = bus.number
            form.brand.data = bus.brand
            form.last_maintenance.data = bus.last_maintenance
            form.next_maintenance.data = bus.next_maintenance
            form.seats_number.data = bus.seats_number
            form.about.data = bus.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        bus = db_sess.query(Bus).filter(Bus.id == bus_id).first()
        if bus:
            bus.number = form.number.data
            bus.brand = form.brand.data
            bus.last_maintenance = form.last_maintenance.data
            bus.next_maintenance = form.next_maintenance.data
            bus.seats_number = form.seats_number.data
            bus.about = form.about.data
            db_sess.commit()
            return redirect('/all_buses')
        else:
            abort(404)
    return render_template('bus.html', form=form, title='Редактирование автобуса')


@login_required
@fapp.route('/delete_bus/<int:bus_id>', methods=['GET', 'POST'])
def delete_bus(bus_id):
    db_sess = db_session.create_session()
    bus = db_sess.query(Bus).filter(Bus.id == bus_id).first()
    if bus:
        db_sess.delete(bus)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/all_buses')


@login_required
@fapp.route('/all_drivers')
def all_drivers():
    db_sess = db_session.create_session()
    drivers = db_sess.query(Driver).all()
    return render_template('all_drivers.html', drivers=drivers, title='Список водителей')


@login_required
@fapp.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    form = DriverForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not form.validate_phone():
            return render_template('driver.html', form=form, message='Неверный номер телефона')
        driver = Driver(
            name=form.name.data,
            surname=form.surname.data,
            lastname=form.lastname.data,
            phone_number=form.phone_number.data
        )
        db_sess.add(driver)
        db_sess.commit()
        return redirect('/all_drivers')
    return render_template('driver.html', form=form, title='Добавление водителя')


@login_required
@fapp.route('/edit_driver/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    form = DriverForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        driver = db_sess.query(Driver).filter(Driver.id == driver_id).first()
        if driver:
            form.name.data = driver.name
            form.surname.data = driver.surname
            form.lastname.data = driver.lastname
            form.phone_number.data = driver.phone_number
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        driver = db_sess.query(Driver).filter(Driver.id == driver_id).first()
        if driver:
            driver.name = form.name.data
            driver.surname = form.surname.data
            driver.lastname = form.lastname.data
            driver.phone_number = form.phone_number.data
            db_sess.commit()
            return redirect('/all_drivers')
        else:
            abort(404)
    return render_template('driver.html', form=form, title='Редактирование водителя')


@login_required
@fapp.route('/delete_driver/<int:driver_id>', methods=['GET', 'POST'])
def delete_driver(driver_id):
    db_sess = db_session.create_session()
    driver = db_sess.query(Driver).filter(Driver.id == driver_id).first()
    if driver:
        db_sess.delete(driver)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/all_drivers')


api.add_resource(drivers_resources.DriversListResource, '/api/drivers')
api.add_resource(drivers_resources.DriverResource, '/api/drivers/<int:driver_id>')
api.add_resource(buses_resources.BusListResource, '/api/buses')
api.add_resource(buses_resources.BusResource, '/api/buses/<int:bus_id>')
api.add_resource(routes_resources.RouteListResource, '/api/routes')
api.add_resource(routes_resources.RouteResource, '/api/routes/<int:route_id>')

print(__name__)
db_session.global_init("db/profile_auto.sqlite")
if __name__ == 'flask_app':
    print("here")
    fapp.run()



