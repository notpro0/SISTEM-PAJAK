"""
app.py
========
File utama SAMSAT PKB Analytics.

Tanggung jawab file ini hanya:
1. Konfigurasi halaman Streamlit
2. Memuat CSS eksternal (assets/style.css)
3. Inisialisasi session_state
4. Menampilkan sidebar & menentukan menu aktif
5. Merutekan (routing) ke halaman yang sesuai di folder pages/

Seluruh logika pemrosesan data, clustering, dan tampilan detail
sudah dipindahkan ke modul-modul di utils/ dan pages/.
"""

import streamlit as st

from pages import (
    analisis_fcm,
    beranda,
    download,
    karakteristik,
    segmentasi,
    upload,
    visualisasi,
)
from utils.helper import init_session_state, muat_css, tampilkan_sidebar

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================

st.set_page_config(
    page_title="SAMSAT PKB Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CSS TAMPILAN DASHBOARD
# ======================================================

muat_css("assets/style.css")

# ======================================================
# SESSION STATE
# ======================================================

init_session_state()

# ======================================================
# SIDEBAR & MENU
# ======================================================

menu = tampilkan_sidebar()

# ======================================================
# ROUTING HALAMAN
# ======================================================

PETA_HALAMAN = {
    "Beranda": beranda.tampilkan,
    "Upload Dataset": upload.tampilkan,
    "Analisis FCM": analisis_fcm.tampilkan,
    "Visualisasi": visualisasi.tampilkan,
    "Karakteristik Cluster": karakteristik.tampilkan,
    "Hasil Segmentasi": segmentasi.tampilkan,
    "Download Hasil": download.tampilkan,
}

PETA_HALAMAN[menu]()
