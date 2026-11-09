"""Tests for the Usage Log feature.
These need the database: run initialise_db.py and populate_db.py first."""
import psycopg2

from config import Config

# product 2 = Fenty Beauty Gloss Bomb, owned by the demo user, 20% in the seed data
PRODUCT_ID = 2
ORIGINAL_PAN = 20


def reset_product():
    conn = psycopg2.connect(Config.DATABASE_URL)
    with conn, conn.cursor() as cur:
        cur.execute("DELETE FROM usage_logs WHERE notes = 'pytest log'")
        cur.execute('UPDATE products SET pan_progress = %s WHERE product_id = %s',
                    (ORIGINAL_PAN, PRODUCT_ID))
    conn.close()


def test_usage_page_lists_products(client):
    response = client.get('/usage')
    assert response.status_code == 200
    assert b'Gloss Bomb Universal Lip Luminizer' in response.data


def test_log_page_shows_history(client):
    response = client.get(f'/usage/{PRODUCT_ID}')
    assert response.status_code == 200
    assert b'Usage History' in response.data


def test_logging_usage_saves_and_updates_product(client):
    reset_product()
    response = client.post(f'/usage/{PRODUCT_ID}',
                           data={'pan_progress': 25, 'notes': 'pytest log'},
                           follow_redirects=True)
    assert b'is now at 25% pan progress' in response.data
    assert b'pytest log' in response.data
    reset_product()


def test_invalid_pan_progress_is_not_saved(client):
    response = client.post(f'/usage/{PRODUCT_ID}', data={'pan_progress': 150})
    assert response.status_code == 200
    assert b'Pan progress must be between 0 and 100.' in response.data


def test_other_users_product_returns_404(client):
    # product 13 belongs to user 2
    assert client.get('/usage/13').status_code == 404


def test_missing_product_returns_404(client):
    assert client.get('/usage/99999').status_code == 404
