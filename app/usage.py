"""Usage logging: record pan progress over time (Use Case 3)."""
from app.db import get_db, query_all, query_one


def get_products_with_usage(user_id):
    """The user's products with how many times each was logged and when it was last logged."""
    return query_all("""
        SELECT p.product_id, p.brand, p.product_name, p.shade, p.category, p.pan_progress,
               COUNT(l.log_id) AS log_count, MAX(l.log_date) AS last_logged
        FROM products p
        LEFT JOIN usage_logs l ON l.product_id = p.product_id
        WHERE p.user_id = %s
        GROUP BY p.product_id
        ORDER BY MAX(l.log_date) DESC NULLS LAST, p.product_name
    """, (user_id,))


def get_product(product_id, user_id):
    """Return one product, only if it belongs to this user."""
    return query_one("""
        SELECT product_id, brand, product_name, shade, category, pan_progress,
               opened_date, expiry_date
        FROM products
        WHERE product_id = %s AND user_id = %s
    """, (product_id, user_id))


def get_usage_history(product_id):
    """Every usage log for a product, newest first."""
    return query_all("""
        SELECT log_date, pan_progress, notes
        FROM usage_logs
        WHERE product_id = %s
        ORDER BY log_date DESC, log_id DESC
    """, (product_id,))


def log_usage(product_id, pan_progress, notes):
    """Save a usage log AND update the product's pan progress in one transaction."""
    conn = get_db()
    with conn:  # both statements commit together, or neither does
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usage_logs (product_id, log_date, pan_progress, notes)
                VALUES (%s, CURRENT_DATE, %s, %s)
            """, (product_id, pan_progress, notes or None))
            cur.execute("""
                UPDATE products SET pan_progress = %s WHERE product_id = %s
            """, (pan_progress, product_id))
