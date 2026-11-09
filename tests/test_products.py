"""Tests for the vault (Home) page and the Add Product / barcode lookup feature.
These need the database: run initialise_db.py and populate_db.py first."""
from datetime import date, timedelta

import psycopg2

from config import Config

TEST_BARCODE = '20999999999'


def delete_test_products():
    conn = psycopg2.connect(Config.DATABASE_URL)
    with conn, conn.cursor() as cur:
        cur.execute('DELETE FROM products WHERE barcode = %s', (TEST_BARCODE,))
    conn.close()


def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'My Vault Collection' in response.data


def test_home_page_lists_products_from_database(client):
    response = client.get('/')
    # owned by the demo user (user 1)
    assert b'Radiant Creamy Concealer' in response.data
    # owned by another user, so must not appear
    assert b'Better Than Sex Mascara' not in response.data


def test_about_page_loads(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About PaletteVault' in response.data


def test_unknown_page_returns_404(client):
    response = client.get('/does-not-exist')
    assert response.status_code == 404


def test_add_product_page_loads(client):
    response = client.get('/products/add')
    assert response.status_code == 200
    assert b'Add a Product' in response.data


def test_known_barcode_fills_in_details(client):
    response = client.get('/products/add?barcode=2100000079193')
    assert b'Barcode found' in response.data
    assert b'NARS Cosmetics' in response.data


def test_unknown_barcode_shows_manual_entry_message(client):
    response = client.get('/products/add?barcode=12345678')
    assert b'Barcode not found' in response.data


def test_add_product_saves_to_database(client):
    delete_test_products()
    response = client.post('/products/add', data={
        'barcode': TEST_BARCODE, 'brand': 'Test Brand', 'product_name': 'Pytest Lip Oil',
        'shade': 'Clear', 'category': 'Lips', 'opened_date': date.today().isoformat(),
        'pao_months': 12, 'pan_progress': 0}, follow_redirects=True)
    assert b'was added to your vault' in response.data
    assert b'Pytest Lip Oil' in response.data
    delete_test_products()


def test_pan_progress_over_100_is_rejected(client):
    response = client.post('/products/add', data={
        'brand': 'Test Brand', 'product_name': 'Bad Pan', 'category': 'Face',
        'opened_date': date.today().isoformat(), 'pao_months': 12, 'pan_progress': 150})
    assert response.status_code == 200
    assert b'Pan progress must be 0 to 100.' in response.data


def test_future_opened_date_is_rejected(client):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response = client.post('/products/add', data={
        'brand': 'Test Brand', 'product_name': 'Future', 'category': 'Face',
        'opened_date': tomorrow, 'pao_months': 12, 'pan_progress': 0})
    assert b'Opened date cannot be in the future.' in response.data
