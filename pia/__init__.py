from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

# Database connection
server = "nombre del servidor"
database = "PIA"
driver = "ODBC+Driver+17+for+SQL+Server"
database_conn = f"mssql+pyodbc://@{server}/{database}?driver={driver}"

# Configuration
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_conn

# Database initialization
db = SQLAlchemy(app)

# Retrieve already created tables in databases
class UserMix(UserMixin):
    def get_id(self):
        return (self.iIdRegistro)

Base = automap_base(cls=UserMix)
Base.prepare(db.engine, reflect=True)


login_manager = LoginManager(app)

from pia import routes