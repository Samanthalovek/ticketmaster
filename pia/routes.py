from flask import render_template, redirect, flash, url_for
from flask_login.utils import login_user, logout_user, current_user
from pia import app, db
from pia.forms import RegisterForm, LoginForm
from pia.models import User

@app.route("/")
def index():
    # users = db.session.query(User).all()

    # for user in users:
    #     print(vars(user))

    return render_template('index.html')


@app.route("/sports")
def sports():
    return render_template('sports.html')


@app.route("/arts")
def arts():
    return render_template('arts.html')


@app.route("/concerts")
def concerts():
    return render_template('concerts.html')


@app.route("/event")
def event():
    return render_template('event.html')


@app.route("/tickets")
def tickets():
    return render_template('tickets.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(Usuario=form.username.data).first()
        if user and user.vContraseña == form.password.data:
            login_user(user)
            flash("Has iniciado sesión", "success")
            return redirect(url_for('index'))
        else:
            flash("Las credenciales no coinciden", "danger")
    return render_template('login.html', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logoutnot ():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_email = db.session.query(User).filter_by(vCorreo=form.email.data).first()
        existing_username = db.session.query(User).filter_by(Usuario=form.username.data).first()
        if not existing_email and not existing_username:
            last_name_1, last_name_2 = form.family_names.data.split(' ')
            new_user = User(
                vNombre=form.names.data,
                vApellidoP=last_name_1,
                vApellidoM=last_name_2,
                vCorreo=form.email.data,
                vContraseña=form.password.data,
                vComprobacion=form.password.data,
                Usuario=form.username.data
            )
            flash("Te has registrado correctamente", "success")
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("Algo salió mal, inténtelo de nuevo", "danger")

    return render_template('register.html', form=form)