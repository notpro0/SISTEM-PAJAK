"""
Halaman Beranda
==================
Menampilkan ringkasan KPI, alur sistem, metode, variabel, dan tujuan sistem.
"""

from datetime import datetime

import streamlit as st


def tampilkan():
    now = datetime.now()

    st.markdown(f"""
    <div class="top-header">
        <div>
            <div class="page-title">Beranda</div>
            <div class="page-subtitle">Sistem Segmentasi Risiko Tunggakan PKB</div>
        </div>
        <div class="date-card">
            <div class="date-icon">▣</div>
            <div>
                <div>{now.strftime("%d-%m-%Y")}</div>
                <div>{now.strftime("%H:%M:%S")} WIB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="hero-label">Selamat datang di</div>
        <div class="hero-title">SAMSAT PKB Analytics</div>
        <div class="hero-desc">
            Sistem ini membantu Anda dalam melakukan analisis data tunggakan PKB
            mulai dari pengolahan data hingga segmentasi risiko untuk mendukung
            pengambilan keputusan yang lebih tepat.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">DB</div>
            <div>
                <div class="kpi-label">Total Data</div>
                <div class="kpi-value">{st.session_state.total_data}</div>
                <div class="kpi-unit">data</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">FCM</div>
            <div>
                <div class="kpi-label">Cluster Optimal</div>
                <div class="kpi-value">{st.session_state.cluster_optimal}</div>
                <div class="kpi-unit">cluster</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">FPC</div>
            <div>
                <div class="kpi-label">Nilai FPC</div>
                <div class="kpi-value">{st.session_state.nilai_fpc}</div>
                <div class="kpi-unit">score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">Rp</div>
            <div>
                <div class="kpi-label">Total Tunggakan</div>
                <div class="kpi-value" style="font-size:22px;">{st.session_state.total_tunggakan}</div>
                <div class="kpi-unit">rupiah</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">HR</div>
            <div>
                <div class="kpi-label">Rata-rata Lama</div>
                <div class="kpi-value">{st.session_state.rata_lama}</div>
                <div class="kpi-unit">hari</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">TM</div>
            <div>
                <div class="kpi-label">Terakhir Proses</div>
                <div class="kpi-value" style="font-size:20px;">{st.session_state.last_process}</div>
                <div class="kpi-unit">waktu</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.45, 1])

    with left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Alur Sistem</div>
            <div class="flow-wrapper">
                <div class="flow-item"><div class="flow-number">1</div><div class="flow-label">Upload<br>Dataset</div></div>
                <div class="flow-item"><div class="flow-number">2</div><div class="flow-label">Transformasi<br>Data</div></div>
                <div class="flow-item"><div class="flow-number">3</div><div class="flow-label">Normalisasi<br>Data</div></div>
                <div class="flow-item"><div class="flow-number">4</div><div class="flow-label">Fuzzy<br>C-Means</div></div>
                <div class="flow-item"><div class="flow-number">5</div><div class="flow-label">Evaluasi<br>FPC</div></div>
                <div class="flow-item"><div class="flow-number">6</div><div class="flow-label">Visualisasi &<br>Segmentasi</div></div>
                <div class="flow-item"><div class="flow-number">7</div><div class="flow-label">Download<br>Excel</div></div>
            </div>
            <div class="info-strip">Ikuti tahapan di atas secara berurutan untuk mendapatkan hasil segmentasi yang optimal.</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Metode</div>
            <p>
            Fuzzy C-Means adalah metode clustering berbasis fuzzy yang memungkinkan
            setiap data menjadi anggota dari setiap cluster dengan derajat keanggotaan tertentu.
            </p>
            <p>
            Evaluasi cluster menggunakan Fuzzy Partition Coefficient (FPC)
            untuk menentukan cluster optimal.
            </p>
        </div>
        """, unsafe_allow_html=True)

    left2, right2 = st.columns([1.15, 1])

    with left2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Variabel yang Digunakan</div>
            <div class="feature-box">
                <div class="feature-badge">H</div>
                <div>
                    <div class="feature-title">Lama Menunggak</div>
                    <div class="feature-desc">Lama waktu wajib pajak menunggak pembayaran PKB dalam satuan hari.</div>
                </div>
            </div>
            <div class="feature-box">
                <div class="feature-badge">Rp</div>
                <div>
                    <div class="feature-title">Total Tunggakan</div>
                    <div class="feature-desc">Total jumlah tunggakan yang harus dibayarkan oleh wajib pajak.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Tujuan Sistem</div>
            <ul>
                <li>Mengidentifikasi pola tunggakan PKB.</li>
                <li>Melakukan segmentasi risiko tunggakan.</li>
                <li>Memberikan rekomendasi tindakan bagi pihak SAMSAT.</li>
                <li>Mendukung pengambilan keputusan berbasis data.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
