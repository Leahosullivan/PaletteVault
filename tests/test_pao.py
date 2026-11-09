"""Unit tests for the PAO expiry helpers (no database needed)."""
from datetime import date

from app.pao import add_months, calculate_expiry, get_status


def test_add_months_simple():
    assert add_months(date(2026, 3, 14), 12) == date(2027, 3, 14)


def test_add_months_clamps_to_end_of_month():
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)


def test_calculate_expiry_mascara():
    assert calculate_expiry(date(2026, 8, 25), 3) == date(2026, 11, 25)


def test_status_fresh():
    assert get_status(date(2027, 1, 1), today=date(2026, 11, 9))[0] == 'Fresh'


def test_status_expiring_soon():
    status, days_left = get_status(date(2026, 11, 16), today=date(2026, 11, 9))
    assert status == 'Expiring Soon'
    assert days_left == 7


def test_status_expired():
    assert get_status(date(2026, 11, 1), today=date(2026, 11, 9))[0] == 'Expired'
