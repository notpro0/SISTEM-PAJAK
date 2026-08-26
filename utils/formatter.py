"""
Modul formatter.py
====================
Berisi fungsi-fungsi bantu untuk memformat tampilan angka
(format rupiah dan format angka ribuan bergaya Indonesia).
"""


def format_rupiah(nilai):
    """Format angka menjadi string rupiah, contoh: Rp 1.250.000"""
    try:
        return "Rp {:,.0f}".format(float(nilai)).replace(",", ".")
    except Exception:
        return "Rp 0"


def format_angka(nilai):
    """Format angka menjadi string dengan pemisah ribuan gaya Indonesia."""
    try:
        return "{:,.0f}".format(float(nilai)).replace(",", ".")
    except Exception:
        return "0"
