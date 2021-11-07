from pia import Base, login_manager, db

# Tables we're going to use
User = Base.classes.Registro

@login_manager.user_loader
def load_user(user_id):
  return db.session.query(User).get(int(user_id))