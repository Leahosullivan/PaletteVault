"""
initialise_db.py - automates creating the PaletteVault database and tables.

Steps:
  1. Connect to the default 'postgres' maintenance database.
  2. Create the 'palettevault' database if it does not already exist.
  3. Connect to 'palettevault' and run database/create_tables.sql.
  4. Print the tables that now exist.

Usage:
  python initialise_db.py
Connection details come from config.py (override with DB_HOST, DB_PORT,
DB_USER, DB_PASSWORD and DB_NAME environment variables).
"""
import os
import sys

import psycopg2
from psycopg2 import sql

from config import Config

SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'database', 'create_tables.sql')


def connect(dbname):
    """Open a connection to the given database using the Config settings."""
    return psycopg2.connect(host=Config.DB_HOST, port=Config.DB_PORT,
                            user=Config.DB_USER, password=Config.DB_PASSWORD,
                            dbname=dbname)


def create_database():
    """Create the application database if it does not exist yet."""
    conn = connect('postgres')
    # CREATE DATABASE cannot run inside a transaction block
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT 1 FROM pg_database WHERE datname = %s', (Config.DB_NAME,))
            if cur.fetchone():
                print(f"Database '{Config.DB_NAME}' already exists.")
            else:
                cur.execute(sql.SQL('CREATE DATABASE {}').format(
                    sql.Identifier(Config.DB_NAME)))
                print(f"Database '{Config.DB_NAME}' created.")
    finally:
        conn.close()


def create_tables():
    """Run the schema file to (re)create every table, key and constraint."""
    with open(SCHEMA_FILE, encoding='utf-8') as f:
        schema = f.read()

    conn = connect(Config.DB_NAME)
    try:
        with conn:  # commits on success, rolls back on error
            with conn.cursor() as cur:
                cur.execute(schema)
                cur.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public' ORDER BY table_name
                """)
                tables = [row[0] for row in cur.fetchall()]
        print('Tables created: ' + ', '.join(tables))
    finally:
        conn.close()


def main():
    try:
        create_database()
        create_tables()
    except psycopg2.OperationalError as error:
        print('Could not connect to PostgreSQL. Is the server running and are the '
              'details in config.py correct?')
        print(error)
        sys.exit(1)
    print('Database initialised. Next step: python populate_db.py')


if __name__ == '__main__':
    main()
