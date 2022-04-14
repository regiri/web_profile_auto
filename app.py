from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/index')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(({'error': 'Not found'})), 404)


@app.route('/register', methods=['GET', 'POST'])
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
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    routes = db_sess.query(Route).all()
    return render_template('index.html', routes=routes, title='Список рейсов')


@login_required
@app.route('/add_bus', methods=['GET', 'POST'])
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
        return redirect('/index')
    return render_template('addbus.html', form=form)


@login_required
@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    form = DriverForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not form.validate_phone():
            return render_template('adddriver.html', form=form, message='Неверный номер телефона')
        driver = Driver(
            name=form.name.data,
            surname=form.surname.data,
            lastname=form.lastname.data,
            phone_number=form.phone_number.data
        )
        db_sess.add(driver)
        db_sess.commit()
        return redirect('/index')
    return render_template('adddriver.html', form=form)


@login_required
@app.route('/add_route', methods=['GET', 'POST'])
def add_route():
    form = RouteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        driver = Route(
            route_name=form.route_name.data,
            start_point=form.start_point.data,
            end_point=form.end_point.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            driver_id=form.driver.data.id,
            bus_id=form.driver.data.id,
            user_id=current_user.id
        )
        db_sess.add(driver)
        db_sess.commit()
        return redirect('/index')
    return render_template('addroute.html', form=form)


if __name__ == 'app':
    db_session.global_init("db/profile_auto.sqlite")


app.run(host='127.0.0.1', port=8080)
