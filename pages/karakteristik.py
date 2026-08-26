"""
Halaman Karakteristik Cluster
================================
Menampilkan ringkasan & statistik deskriptif tiap cluster, distribusi
anggota cluster, dan karakteristik kendaraan per cluster (Merk, Jenis,
Tipe Kendaraan) jika kolomnya tersedia pada dataset, sesuai bagian
"4.8 Analisis Karakteristik Kendaraan Berdasarkan Hasil Clustering"
pada notebook final "FCM17.ipynb".

Catatan: kolom Merk Kendaraan bernama "MERK". Kolom Tahun Kendaraan
sudah tidak lagi dianalisis pada notebook terbaru sehingga tidak
ditampilkan di halaman ini.
"""

import matplotlib.pyplot as plt
import streamlit as st

from utils.clustering import hitung_karakteristik_kategori, kolom_kategori_tersedia


def _tampilkan_kategori(df, kolom, label):
    with st.container(border=True):
        st.markdown(f'<div class="card-title">{label} per Cluster</div>', unsafe_allow_html=True)

        hasil = hitung_karakteristik_kategori(df, kolom)

        tab_labels = [f"Cluster {c}" for c in hasil.keys()]
        tabs = st.tabs(tab_labels)

        for tab, (c, data_cluster) in zip(tabs, hasil.items()):
            with tab:
                col_tabel, col_grafik = st.columns([1, 1.2])

                with col_tabel:
                    st.dataframe(data_cluster, use_container_width=True)

                with col_grafik:
                    if len(data_cluster) > 0:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        ax.bar(data_cluster[kolom].astype(str), data_cluster["Jumlah"], color="#0b63ce")
                        ax.set_title(f"Top {len(data_cluster)} {label} - Cluster {c}")
                        ax.set_xlabel(label)
                        ax.set_ylabel("Jumlah Wajib Pajak")
                        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

                        for i, v in enumerate(data_cluster["Jumlah"]):
                            ax.text(i, v, str(v), ha="center", va="bottom", fontsize=9)

                        fig.tight_layout()
                        st.pyplot(fig)


def tampilkan():
    st.markdown('<div class="page-title">Karakteristik Cluster</div>', unsafe_allow_html=True)

    if st.session_state.hasil_fcm is None:
        st.warning("Silakan upload dan proses dataset terlebih dahulu.")
        return

    df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik, distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi = st.session_state.hasil_fcm

    with st.container(border=True):
        st.markdown('<div class="card-title">Ringkasan Karakteristik Cluster (Nilai Asli)</div>', unsafe_allow_html=True)
        st.dataframe(ringkasan_karakteristik, use_container_width=True)
        st.caption(
            "Ringkasan jumlah data, rata-rata Lama Menunggak (hari), dan rata-rata "
            "Total Tunggakan (Rp) per cluster, memakai nilai asli (bukan hasil normalisasi)."
        )

    with st.container(border=True):
        st.markdown('<div class="card-title">Statistik Deskriptif Lengkap</div>', unsafe_allow_html=True)
        st.dataframe(karakteristik, use_container_width=True)

    with st.container(border=True):
        st.markdown('<div class="card-title">Distribusi Anggota Cluster</div>', unsafe_allow_html=True)
        st.dataframe(distribusi, use_container_width=True)

    kolom_kategori = kolom_kategori_tersedia(df)

    if not kolom_kategori:
        st.info(
            "Kolom karakteristik kendaraan (MERK, TIPE, MODEL) "
            "tidak ditemukan pada dataset yang diupload, sehingga analisis ini dilewati."
        )
        return

    st.markdown('<div class="page-subtitle" style="margin-top:10px;">Karakteristik Kendaraan per Cluster</div>', unsafe_allow_html=True)

    for kolom, label in kolom_kategori:
        _tampilkan_kategori(df, kolom, label)
