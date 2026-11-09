# import from package Flask
from flask import Flask
# import config from Config
from config import Config

# create an app variable to store the __name__ passed from the Flask class
app = Flask(__name__)

# request Flask to read and apply Config class
app.config.from_object(Config)

# import routes module from the app package (at the bottom to avoid circular imports)
from app import routes  # noqa: E402,F401
