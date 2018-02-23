from flask import Flask
from config import Config
from Database_initial_connection import connect_for_table_and_database_creation
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes
