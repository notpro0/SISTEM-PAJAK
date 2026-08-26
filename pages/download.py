"""
Halaman Download Hasil
=========================
Menyusun dan menyediakan tombol unduh file Excel hasil analisis lengkap.
"""

import streamlit as st

from utils.excel_export import buat_excel_hasil


def tampilkan():
    st.markdown('<div class="page-title">Download Hasil</div>', unsafe_allow_html=True)

    if st.session_state.hasil_fcm is None:
        st.warning("Silakan upload dan proses dataset terlebih dahulu.")
        return

    df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik, distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi = st.session_state.hasil_fcm

    file_excel = buat_excel_hasil(
        df,
        df_fpc,
        centroid_df,
        karakteristik,
        distribusi,
        ringkasan_karakteristik
    )

    st.markdown("""
    <div class="card">
        <div class="card-title">Export Hasil Segmentasi</div>
        <p>
        File Excel berisi data asli SAMSAT dan kolom tambahan hasil analisis:
        LAMA_HARI, normalisasi, membership cluster, cluster, segmentasi, prioritas,
        dan rekomendasi tindakan SAMSAT — lengkap dengan sheet terpisah untuk
        Cluster 0 dan Cluster 1 (diurutkan dari Lama Menunggak terlama).
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Download Excel Hasil Segmentasi",
        data=file_excel,
        file_name="Hasil_Segmentasi_PKB_SAMSAT.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
