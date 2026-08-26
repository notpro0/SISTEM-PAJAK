"""
Halaman Visualisasi
======================
Menampilkan berbagai grafik hasil clustering:
korelasi Pearson, scatter plot, distribusi cluster, boxplot,
histogram membership, dan grafik evaluasi FPC.

Setiap grafik dilengkapi keterangan singkat di bawahnya supaya lebih
mudah dibaca oleh pengguna yang tidak terlalu teknis.

Disesuaikan dengan notebook "FCM17.ipynb":
- Scatter plot memakai palette "Set1" (bukan "Blues").
- Tab Korelasi Pearson (heatmap), sesuai tahap uji korelasi Pearson notebook.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from utils.preprocessing import hitung_korelasi

# Warna tetap untuk tiap cluster: Cluster 0 = merah, Cluster 1 = kuning.
# Dipakai di semua grafik pada halaman ini supaya warnanya konsisten.
WARNA_CLUSTER = {0: "#e63946", 1: "#f4d35e"}


def _label_kekuatan_korelasi(nilai):
    """Menerjemahkan angka korelasi Pearson menjadi keterangan kekuatan hubungan."""
    nilai_abs = abs(nilai)

    if nilai_abs >= 0.8:
        kekuatan = "sangat kuat"
    elif nilai_abs >= 0.6:
        kekuatan = "kuat"
    elif nilai_abs >= 0.4:
        kekuatan = "sedang"
    elif nilai_abs >= 0.2:
        kekuatan = "lemah"
    else:
        kekuatan = "sangat lemah / hampir tidak berhubungan"

    arah = "searah (positif)" if nilai >= 0 else "berlawanan arah (negatif)"
    return kekuatan, arah


def tampilkan():
    st.markdown('<div class="page-title">Visualisasi</div>', unsafe_allow_html=True)

    if st.session_state.hasil_fcm is None:
        st.warning("Silakan upload dan proses dataset terlebih dahulu.")
        return

    df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik, distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi = st.session_state.hasil_fcm

    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Korelasi Pearson",
        "Scatter Plot",
        "Distribusi Cluster",
        "Boxplot",
        "Membership FCM",
        "Evaluasi FPC"
    ])

    # ==================================================================
    # TAB 0 - KORELASI PEARSON
    # ==================================================================
    with tab0:
        with st.container(border=True):
            corr_matrix = hitung_korelasi(df)

            col_heatmap, col_tabel = st.columns([1.3, 1])

            with col_heatmap:
                fig, ax = plt.subplots(figsize=(7, 5.5))
                sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".3f", ax=ax)
                ax.set_title("Heatmap Korelasi Pearson")
                st.pyplot(fig)

            with col_tabel:
                st.markdown("**Matriks Korelasi Pearson**")
                st.dataframe(corr_matrix.round(3), use_container_width=True)

            if "LAMA_HARI" in corr_matrix.columns and "TOTAL TUNGGAKAN" in corr_matrix.columns:
                nilai_r = corr_matrix.loc["LAMA_HARI", "TOTAL TUNGGAKAN"]
                kekuatan, arah = _label_kekuatan_korelasi(nilai_r)
                st.caption(
                    f"**Keterangan:** Heatmap ini menunjukkan seberapa erat hubungan antar variabel numerik "
                    f"(semakin mendekati 1 atau -1, semakin erat; semakin mendekati 0, semakin tidak berhubungan). "
                    f"Nilai korelasi antara Lama Menunggak dan Total Tunggakan adalah **{nilai_r:.3f}**, "
                    f"artinya hubungan keduanya tergolong **{kekuatan}** dan **{arah}**."
                )

    # ==================================================================
    # TAB 1 - SCATTER PLOT
    # ==================================================================
    with tab1:
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.scatterplot(
                data=df,
                x="LAMA_HARI",
                y="TOTAL TUNGGAKAN",
                hue="CLUSTER",
                palette=WARNA_CLUSTER,
                alpha=0.75,
                ax=ax
            )
            ax.set_title("Scatter Plot Hasil Clustering")
            ax.set_xlabel("Lama Menunggak (Hari)")
            ax.set_ylabel("Total Tunggakan")
            st.pyplot(fig)
            st.caption(
                "**Keterangan:** Setiap titik mewakili satu wajib pajak, diposisikan berdasarkan "
                "lama menunggak (sumbu X) dan total tunggakan (sumbu Y). Warna titik menunjukkan "
                "cluster hasil Fuzzy C-Means — titik yang warnanya sama cenderung memiliki pola "
                "tunggakan yang mirip, dan titik yang mengumpul menandakan kelompok data yang serupa."
            )

    # ==================================================================
    # TAB 2 - DISTRIBUSI CLUSTER
    # ==================================================================
    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(7, 4))
                warna_bar = [WARNA_CLUSTER.get(int(c), "#999999") for c in distribusi["Cluster"]]
                distribusi.plot(x="Cluster", y="Jumlah Data", kind="bar", ax=ax, legend=False, color=warna_bar)
                ax.set_title("Distribusi Data pada Setiap Cluster")
                ax.set_xlabel("Cluster")
                ax.set_ylabel("Jumlah Data")
                st.pyplot(fig)
                st.caption(
                    "**Keterangan:** Grafik batang ini menunjukkan jumlah wajib pajak pada "
                    "masing-masing cluster. Semakin tinggi batang, semakin banyak data yang "
                    "termasuk ke dalam cluster tersebut."
                )

        with col2:
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(6, 4))
                warna_pie = [WARNA_CLUSTER.get(int(c), "#999999") for c in distribusi["Cluster"]]
                ax.pie(
                    distribusi["Jumlah Data"],
                    labels=distribusi["Cluster"],
                    autopct="%1.1f%%",
                    colors=warna_pie
                )
                ax.set_title("Proporsi Anggota Cluster")
                st.pyplot(fig)

                baris_terbesar = distribusi.loc[distribusi["Jumlah Data"].idxmax()]
                st.caption(
                    f"**Keterangan:** Diagram lingkaran ini menunjukkan proporsi (persentase) "
                    f"jumlah data di tiap cluster terhadap keseluruhan data. Cluster "
                    f"**{int(baris_terbesar['Cluster'])}** memiliki proporsi terbesar, yaitu "
                    f"**{baris_terbesar['Persentase']}%** dari total data."
                )

    # ==================================================================
    # TAB 3 - BOXPLOT
    # ==================================================================
    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(7, 4))
                sns.boxplot(data=df, x="CLUSTER", y="LAMA_HARI", hue="CLUSTER", palette=WARNA_CLUSTER, legend=False, ax=ax)
                ax.set_title("Boxplot Lama Menunggak")
                ax.set_xlabel("Cluster")
                ax.set_ylabel("Lama Menunggak")
                st.pyplot(fig)
                st.caption(
                    "**Keterangan:** Kotak (box) menunjukkan sebaran nilai Lama Menunggak pada "
                    "tiap cluster — garis tengah kotak adalah nilai median, tepi kotak adalah "
                    "kuartil bawah dan atas, sementara titik-titik di luar garis adalah data "
                    "yang nilainya jauh berbeda dari mayoritas (outlier)."
                )

        with col2:
            with st.container(border=True):
                fig, ax = plt.subplots(figsize=(7, 4))
                sns.boxplot(data=df, x="CLUSTER", y="TOTAL TUNGGAKAN", hue="CLUSTER", palette=WARNA_CLUSTER, legend=False, ax=ax)
                ax.set_title("Boxplot Total Tunggakan")
                ax.set_xlabel("Cluster")
                ax.set_ylabel("Total Tunggakan")
                st.pyplot(fig)
                st.caption(
                    "**Keterangan:** Sama seperti boxplot di sebelah kiri, tetapi untuk variabel "
                    "Total Tunggakan. Kotak yang letaknya lebih tinggi menandakan cluster tersebut "
                    "cenderung memiliki nominal tunggakan yang lebih besar."
                )

    # ==================================================================
    # TAB 4 - MEMBERSHIP FCM
    # ==================================================================
    with tab4:
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(10, 5))
            for i in range(cluster_optimal):
                ax.hist(u[i], bins=30, alpha=0.6, label=f"Cluster {i}", color=WARNA_CLUSTER.get(i, "#999999"))
            ax.set_title("Distribusi Membership Fuzzy C-Means")
            ax.set_xlabel("Derajat Keanggotaan")
            ax.set_ylabel("Jumlah Data")
            ax.legend()
            st.pyplot(fig)
            st.caption(
                "**Keterangan:** Grafik ini menunjukkan derajat keanggotaan (membership) tiap "
                "data terhadap suatu cluster, dengan nilai antara 0 sampai 1. Nilai mendekati 1 "
                "berarti data tersebut sangat yakin/kuat menjadi anggota cluster itu, sedangkan "
                "nilai mendekati 0.5 berarti data berada di posisi 'abu-abu' — cukup mirip dengan "
                "kedua cluster sekaligus. Inilah ciri khas Fuzzy C-Means dibanding clustering biasa."
            )

    # ==================================================================
    # TAB 5 - EVALUASI FPC
    # ==================================================================
    with tab5:
        with st.container(border=True):
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.lineplot(data=df_fpc, x="Jumlah Cluster", y="FPC", marker="o", ax=ax)
            ax.set_title("Evaluasi FPC (perbandingan c=2..5)")
            ax.set_xlabel("Jumlah Cluster")
            ax.set_ylabel("Nilai FPC")
            st.pyplot(fig)
            st.caption(
                f"**Keterangan:** FPC (Fuzzy Partition Coefficient) mengukur seberapa jelas/tegas "
                f"pemisahan antar cluster — nilai berkisar 0 sampai 1, semakin tinggi semakin baik "
                f"pemisahannya. Grafik ini membandingkan nilai FPC untuk jumlah cluster 2 sampai 5 "
                f"sebagai referensi, dengan nilai FPC pada cluster final (c = {cluster_optimal}) "
                f"sebesar **{fpc_final:.4f}**. Clustering final tetap memakai c = 2 sesuai pipeline "
                f"pada notebook penelitian, walaupun nilai FPC di jumlah cluster lain mungkin "
                f"terlihat lebih tinggi."
            )
