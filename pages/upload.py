"""
Halaman Upload Dataset
=========================
Menerima file Excel dari pengguna, menampilkan preview,
mengecek missing value/duplikat, memvalidasi kolom wajib,
lalu menjalankan pipeline Fuzzy C-Means.
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from utils.clustering import proses_data_fcm
from utils.formatter import format_angka, format_rupiah
from utils.preprocessing import cek_data_kosong_dan_duplikat, kolom_wajib_lengkap


def tampilkan():
    st.markdown('<div class="page-title">Upload Dataset</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Upload Data Tunggakan Pajak Kendaraan Bermotor</div>
        <p>
        Silakan upload file Excel data tunggakan PKB. Sistem akan melakukan transformasi,
        normalisasi, proses Fuzzy C-Means, evaluasi FPC, segmentasi risiko, dan rekomendasi tindakan.
        </p>
        <p>
        Kolom wajib: <b>LAMA MENUNGGAK</b>, <b>POKOK</b>, <b>DENDA</b>.
        Kolom <b>TOTAL TUNGGAKAN</b> akan dihitung ulang otomatis sebagai POKOK + DENDA
        agar konsisten dengan data asli.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])

    if uploaded_file is not None:
        df_awal = pd.read_excel(uploaded_file)

        with st.container(border=True):
            st.markdown('<div class="card-title">Preview Dataset</div>', unsafe_allow_html=True)
            st.write("Jumlah data:", len(df_awal))
            st.dataframe(df_awal.head(), use_container_width=True)

        if not kolom_wajib_lengkap(df_awal):
            st.error("Kolom wajib tidak lengkap. Pastikan tersedia kolom LAMA MENUNGGAK, POKOK, dan DENDA.")
            st.stop()

        # Data cleaning check (missing value & duplikat), sesuai notebook.
        missing, jumlah_duplikat = cek_data_kosong_dan_duplikat(df_awal)
        total_missing = int(missing.sum())

        with st.expander("Cek Data Kosong & Duplikat (Data Cleaning)"):
            colm, cold = st.columns(2)
            with colm:
                st.write("Jumlah missing value per kolom:")
                st.dataframe(missing[missing > 0] if total_missing > 0 else missing, use_container_width=True)
            with cold:
                st.metric("Total Missing Value", format_angka(total_missing))
                st.metric("Jumlah Data Duplikat", format_angka(jumlah_duplikat))

        if st.button("Proses Dataset", use_container_width=True):
            with st.spinner("Sedang memproses data..."):
                hasil = proses_data_fcm(df_awal)
                st.session_state.hasil_fcm = hasil

                df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik, distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi = hasil

                st.session_state.total_data = format_angka(len(df))
                st.session_state.cluster_optimal = cluster_optimal
                st.session_state.nilai_fpc = round(fpc_final, 6)
                st.session_state.total_tunggakan = format_rupiah(df["TOTAL TUNGGAKAN"].sum())
                st.session_state.rata_lama = format_angka(df["LAMA_HARI"].mean())
                st.session_state.last_process = datetime.now().strftime("%H:%M")

            st.success("Dataset berhasil diproses. Silakan buka menu Analisis FCM, Visualisasi, Karakteristik Cluster, Hasil Segmentasi, atau Download Hasil.")
