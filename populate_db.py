"""
populate_db.py - automates populating the PaletteVault tables.

Reads the CSV files in data/ and inserts them into the database created by
initialise_db.py. Any existing rows are removed first, so the script can be
re-run to reset the data.

  data/users.csv           -> users          (passwords are hashed first)
  data/products.csv        -> products       (expiry date and status calculated)
  data/usage_logs.csv      -> usage_logs
  data/wishlist_items.csv  -> wishlist_items

Usage:
  python populate_db.py
"""
import csv
import os
import sys
from datetime import date

import psycopg2
from werkzeug.security import generate_password_hash

from config import Config
from app.pao import calculate_expiry, get_status

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TABLES = ['users', 'products', 'usage_logs', 'wishlist_items']


def read_csv(filename):
    """Return the rows of a CSV file in data/ as a list of dictionaries."""
    with open(os.path.join(DATA_DIR, filename), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def insert_users(cur):
    rows = read_csv('users.csv')
    for row in rows:
        cur.execute(
            """INSERT INTO users (user_id, username, email, password_hash, created_at)
               VALUES (%s, %s, %s, %s, %s)""",
            (row['user_id'], row['username'], row['email'],
             generate_password_hash(row['password']), row['created_at']))
    return len(rows)


def insert_products(cur):
    rows = read_csv('products.csv')
    for row in rows:
        opened = date.fromisoformat(row['opened_date'])
        expiry = calculate_expiry(opened, int(row['pao_months']))
        status, _ = get_status(expiry)
        cur.execute(
            """INSERT INTO products (product_id, user_id, brand, product_name, shade,
                   category, barcode, opened_date, pao_months, expiry_date,
                   pan_progress, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (row['product_id'], row['user_id'], row['brand'], row['product_name'],
             row['shade'], row['category'], row['barcode'], opened,
             row['pao_months'], expiry, row['pan_progress'], status))
    return len(rows)


def insert_usage_logs(cur):
    rows = read_csv('usage_logs.csv')
    for row in rows:
        cur.execute(
            """INSERT INTO usage_logs (log_id, product_id, log_date, pan_progress, notes)
               VALUES (%s, %s, %s, %s, %s)""",
            (row['log_id'], row['product_id'], row['log_date'],
             row['pan_progress'], row['notes']))
    return len(rows)


def insert_wishlist_items(cur):
    rows = read_csv('wishlist_items.csv')
    for row in rows:
        cur.execute(
            """INSERT INTO wishlist_items (wishlist_id, user_id, brand, product_name,
                   shade, category, added_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (row['wishlist_id'], row['user_id'], row['brand'], row['product_name'],
             row['shade'], row['category'], row['added_date']))
    return len(rows)


def reset_sequences(cur):
    """Move each SERIAL counter past the IDs inserted from the CSV files."""
    for table, column in [('users', 'user_id'), ('products', 'product_id'),
                          ('usage_logs', 'log_id'), ('wishlist_items', 'wishlist_id')]:
        cur.execute(f"SELECT setval(pg_get_serial_sequence('{table}', '{column}'), "
                    f"COALESCE(MAX({column}), 1)) FROM {table}")


def main():
    try:
        conn = psycopg2.connect(Config.DATABASE_URL)
    except psycopg2.OperationalError as error:
        print('Could not connect to the database. Run initialise_db.py first.')
        print(error)
        sys.exit(1)

    try:
        with conn:  # one transaction: everything is inserted or nothing is
            with conn.cursor() as cur:
                cur.execute('TRUNCATE ' + ', '.join(TABLES) + ' RESTART IDENTITY CASCADE')
                # parents first so the foreign keys are satisfied
                counts = {
                    'users': insert_users(cur),
                    'products': insert_products(cur),
                    'usage_logs': insert_usage_logs(cur),
                    'wishlist_items': insert_wishlist_items(cur),
                }
                reset_sequences(cur)
    finally:
        conn.close()

    for table, count in counts.items():
        print(f'{table:<15} {count:>3} rows inserted')
    print('Database populated.')


if __name__ == '__main__':
    main()
