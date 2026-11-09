# import os to allow for interaction with environment variables in the operating system
import os


# create class to hold config data for web service
class Config:
    # define secret key (used by Flask-WTF to protect forms against CSRF)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'P4L3TT3V4ULT'

    # PostgreSQL connection details (defaults match tech_spec.yaml)
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'postgres'
    DB_NAME = os.environ.get('DB_NAME') or 'palettevault'

    # full connection string used by the app (Render supplies DATABASE_URL)
    DATABASE_URL = os.environ.get('DATABASE_URL') or \
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # until Flask-Login is added, the vault pages show this user's products
    DEMO_USER_ID = int(os.environ.get('DEMO_USER_ID') or 1)
