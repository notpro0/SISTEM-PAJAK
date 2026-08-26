"""
Modul helper.py
==================
Berisi fungsi-fungsi bantu umum untuk app.py:
- memuat CSS eksternal
- menampilkan sidebar & menu navigasi
- inisialisasi session_state
"""

import base64
from pathlib import Path

import streamlit as st

DAFTAR_MENU = [
    "Beranda",
    "Upload Dataset",
    "Analisis FCM",
    "Visualisasi",
    "Karakteristik Cluster",
    "Hasil Segmentasi",
    "Download Hasil",
]


def muat_css(path_css="assets/style.css"):
    """Membaca file CSS eksternal dan menyuntikkannya ke halaman Streamlit."""
    css_path = Path(path_css)

    if css_path.exists():
        css_text = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)


def _logo_base64(path_logo="assets/logo.png"):
    """Membaca file logo dan meng-encode-nya ke base64 agar bisa ditampilkan
    lewat tag <img> di dalam HTML kustom (Streamlit tidak bisa memuat file
    lokal langsung lewat path biasa)."""
    logo_path = Path(path_logo)

    if logo_path.exists():
        data = logo_path.read_bytes()
        return base64.b64encode(data).decode("utf-8")

    return None


def tampilkan_sidebar():
    """Menampilkan brand, menu navigasi, dan info sistem di sidebar. Mengembalikan menu terpilih."""
    logo_b64 = _logo_base64()

    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img" alt="Logo SAMSAT">'
    else:
        # Fallback kalau assets/logo.png belum tersedia.
        logo_html = '<div class="logo-text">S</div>'

    st.sidebar.markdown(f"""
    <div class="sidebar-brand">
        <div class="logo-row">
            <div class="logo-box">{logo_html}</div>
            <div>
                <div class="brand-title">SAMSAT</div>
                <div class="brand-subtitle">PKB Analytics</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="sidebar-section">MENU UTAMA</div>', unsafe_allow_html=True)

    menu = st.sidebar.radio(
        "Menu",
        DAFTAR_MENU,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("""
    <div class="sidebar-info">
    <b>TENTANG SISTEM</b><br><br>
    Dashboard ini digunakan untuk menganalisis dan melakukan segmentasi risiko tunggakan
    Pajak Kendaraan Bermotor menggunakan metode Fuzzy C-Means.
    <br><br>
    UPT SAMSAT SIMPANG TIGA PEKANBARU<br>
    © 2026
    </div>
    """, unsafe_allow_html=True)

    return menu


def init_session_state():
    """Menginisialisasi seluruh key session_state yang dipakai lintas halaman."""
    default_state = {
        "hasil_fcm": None,
        "total_data": 0,
        "cluster_optimal": "-",
        "nilai_fpc": "-",
        "total_tunggakan": "Rp 0",
        "rata_lama": 0,
        "last_process": "-",
    }

    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value
