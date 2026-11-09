"""PAO (Period After Opening) helpers shared by the app and populate_db.py."""
import calendar
from datetime import date

# a product is "Expiring Soon" when this many days or fewer are left
EXPIRING_SOON_DAYS = 30


def add_months(start, months):
    """Return the date `months` after `start` (clamped to the end of the month)."""
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def calculate_expiry(opened_date, pao_months):
    """Expiry date = opened date + PAO months."""
    return add_months(opened_date, pao_months)


def get_status(expiry_date, today=None):
    """Return (status, days_left) for a product's expiry date."""
    today = today or date.today()
    days_left = (expiry_date - today).days
    if days_left < 0:
        return 'Expired', days_left
    if days_left <= EXPIRING_SOON_DAYS:
        return 'Expiring Soon', days_left
    return 'Fresh', days_left
