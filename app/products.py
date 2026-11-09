"""Product queries for the vault: list, barcode lookup and add (Use Cases 1 and 2)."""
from app.db import get_db, query_all, query_one
from app.pao import EXPIRING_SOON_DAYS, calculate_expiry, get_status


def refresh_statuses(user_id):
    """Recalculate Fresh / Expiring Soon / Expired against today's date and save any changes."""
    conn = get_db()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE products SET status = CASE
                    WHEN expiry_date < CURRENT_DATE THEN 'Expired'
                    WHEN expiry_date <= CURRENT_DATE + %s THEN 'Expiring Soon'
                    ELSE 'Fresh' END
                WHERE user_id = %s
            """, (EXPIRING_SOON_DAYS, user_id))


def get_vault(user_id):
    """Return the user's products, soonest expiry first, with days left added."""
    refresh_statuses(user_id)
    products = query_all("""
        SELECT product_id, brand, product_name, shade, category, barcode,
               opened_date, pao_months, expiry_date, pan_progress, status
        FROM products
        WHERE user_id = %s
        ORDER BY expiry_date, product_name
    """, (user_id,))
    for product in products:
        product['status'], product['days_left'] = get_status(product['expiry_date'])
    return products


def find_by_barcode(barcode):
    """Look up product details already stored for this barcode (any user)."""
    return query_one("""
        SELECT brand, product_name, shade, category, pao_months
        FROM products
        WHERE barcode = %s
        ORDER BY product_id
        LIMIT 1
    """, (barcode,))


def add_product(user_id, data):
    """Insert a new product; expiry date and status are calculated here. Returns the new ID."""
    expiry = calculate_expiry(data['opened_date'], data['pao_months'])
    status, _ = get_status(expiry)
    conn = get_db()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (user_id, brand, product_name, shade, category,
                    barcode, opened_date, pao_months, expiry_date, pan_progress, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING product_id
            """, (user_id, data['brand'], data['product_name'], data['shade'] or None,
                  data['category'], data['barcode'] or None, data['opened_date'],
                  data['pao_months'], expiry, data['pan_progress'], status))
            return cur.fetchone()[0]
