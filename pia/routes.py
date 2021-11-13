from flask import render_template, redirect, flash, url_for, request
from flask_login.utils import login_user, logout_user, current_user
from werkzeug.exceptions import BadRequestKeyError
from pia import app, db
from pia.forms import BuyForm, RegisterForm, LoginForm
from pia.models import User, Event, Ticket
from pia.utils import set_image_path, get_place


def get_events(category, video):
    events = db.session.query(Event).filter_by(
        iIdTipoEvent=category
    ).all() if category else db.session.query(Event).all()
    return render_template(
        "index.html",
        events=events,
        video=video,
        set_image=set_image_path,
        get_place=get_place
    )


@app.route("/")
@app.route("/events")
def index():
    return get_events(None, "video/bg.mp4")


@app.route("/sports")
def sports():
    return get_events(2, "video/sports.mp4")


@app.route("/arts")
def arts():
    return get_events(3, "video/arts.mp4")


@app.route("/concerts")
def concerts():
    return get_events(1, "video/concerts.mp4")


@app.route("/events/<int:id>")
def event(id):
    event = db.session.query(Event).filter_by(
        iIdEvento=id
    ).first()
    file = set_image_path(id)
    return render_template(
        'events.html',
        event=event,
        filename=file,
        get_place=get_place
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(
            Usuario=form.username.data).first()
        if user and user.vContraseña == form.password.data:
            login_user(user)
            flash("Has iniciado sesión", "success")
            return redirect(url_for('index'))
        else:
            flash("Las credenciales no coinciden", "danger")

    return render_template('login.html', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_email = db.session.query(User).filter_by(
            vCorreo=form.email.data).first()
        existing_username = db.session.query(User).filter_by(
            Usuario=form.username.data).first()
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


def tickets_count(tickets):
    result = {}
    for ticket in tickets:
        if (id := ticket.iIdEvento) not in result:
            result[id] = 1
        else:
            result[id] += 1

    return result


def tickets_events(tickets):
    result = []
    for event_id in tickets:
        event = db.session.query(Event).filter_by(iIdEvento=event_id).first()
        result.append(event)

    return result


@app.route("/tickets")
def tickets():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))

    tickets = db.session.query(Ticket).filter_by(
        iIdRegistro=current_user.iIdRegistro
    ).all()

    tickets = tickets_count(tickets)
    events = tickets_events(tickets)

    return render_template(
        'tickets.html',
        tickets=tickets,
        events=events,
        set_image=set_image_path,
        get_place=get_place
    )


@app.route("/buy", methods=["GET", "POST"])
def buy():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    id = 0
    try:
        id = int(request.args['id'])
    except BadRequestKeyError:
        id = 1
    except ValueError:
        id = 1

    event = db.session.query(Event).filter_by(
        iIdEvento=id
    ).first()

    if not event:
        flash("No existe el evento del cual intenta comprar boletos")
        return redirect(url_for("index"))

    form = BuyForm()
    if form.validate_on_submit():
        event.iCantBole -= 1
        new_ticket = Ticket(
            iIdRegistro=current_user.iIdRegistro,
            iIdEvento=event.iIdEvento
        )
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for("tickets"))

    return render_template(
        "buy.html",
        event=event,
        get_place=get_place,
        file_path=set_image_path,
        form=form
    )
