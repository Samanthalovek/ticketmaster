from pia import Base, login_manager, db


# Tables we're going to use
User = Base.classes.Registro
Event = Base.classes.Evento
Place = Base.classes.Lugar
Ticket = Base.classes.Boleto


@login_manager.user_loader
def load_user(user_id):
  return db.session.query(User).get(int(user_id))