"""
Halaman Analisis FCM
=======================
Menampilkan KPI ringkas, tabel konvergensi, evaluasi FPC, centroid,
statistik ringkas, dan radar chart dari hasil proses Fuzzy C-Means
yang tersimpan di session_state.
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from utils.formatter import format_angka, format_rupiah


def tampilkan():
    st.markdown('<div class="page-title">Analisis FCM</div>', unsafe_allow_html=True)

    if st.session_state.hasil_fcm is None:
        st.warning("Silakan upload dan proses dataset terlebih dahulu.")
        return

    df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik, distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi = st.session_state.hasil_fcm

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">DB</div>
            <div>
                <div class="kpi-label">Jumlah Data</div>
                <div class="kpi-value">{format_angka(len(df))}</div>
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
                <div class="kpi-value">{cluster_optimal}</div>
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
                <div class="kpi-value">{round(fpc_final, 6)}</div>
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
                <div class="kpi-value" style="font-size:22px;">{format_rupiah(df["TOTAL TUNGGAKAN"].sum())}</div>
                <div class="kpi-unit">rupiah</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="card-title">Hasil Pengujian Konvergensi FCM</div>', unsafe_allow_html=True)
        st.dataframe(tabel_konvergensi, use_container_width=True)
        st.caption(
            "Menunjukkan nilai fungsi objektif (J) pada iterasi pertama dan terakhir, "
            "serta jumlah iterasi yang dibutuhkan sampai konvergen, untuk tiap kandidat "
            "jumlah cluster (c = 2 sampai 5)."
        )

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown('<div class="card-title">Evaluasi Fuzzy Partition Coefficient</div>', unsafe_allow_html=True)
            st.dataframe(df_fpc, use_container_width=True)
            st.caption(
                "Tabel ini membandingkan nilai FPC untuk c = 2 sampai 5 sebagai referensi. "
                "Clustering final tetap memakai c = 2 sesuai pipeline pada notebook penelitian."
            )

    with right:
        with st.container(border=True):
            st.markdown('<div class="card-title">Nilai Centroid Cluster</div>', unsafe_allow_html=True)
            st.dataframe(centroid_df, use_container_width=True)

    with st.container(border=True):
        st.markdown('<div class="card-title">Statistik Ringkas Lama Menunggak (Hari)</div>', unsafe_allow_html=True)

        stat1, stat2, stat3 = st.columns(3)
        with stat1:
            st.metric("Minimum", f"{format_angka(df['LAMA_HARI'].min())} hari")
        with stat2:
            st.metric("Rata-rata", f"{format_angka(df['LAMA_HARI'].mean())} hari")
        with stat3:
            st.metric("Maksimum", f"{format_angka(df['LAMA_HARI'].max())} hari")

    with st.container(border=True):
        st.markdown('<div class="card-title">Radar Chart Centroid</div>', unsafe_allow_html=True)

        kolom_radar = [k for k in centroid_df.columns if k != "CLUSTER"]
        labels = kolom_radar
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})

        for c in centroid_df["CLUSTER"]:
            nilai = centroid_df.loc[centroid_df["CLUSTER"] == c, kolom_radar].values.flatten()
            nilai = np.concatenate((nilai, [nilai[0]]))
            ax.plot(angles, nilai, linewidth=2, label=f"Cluster {c}")
            ax.fill(angles, nilai, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title("Radar Chart Centroid")
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

        st.pyplot(fig)
        st.caption("Membandingkan posisi centroid tiap cluster pada variabel LAMA_HARI dan TOTAL TUNGGAKAN yang sudah dinormalisasi (skala 0-1).")
