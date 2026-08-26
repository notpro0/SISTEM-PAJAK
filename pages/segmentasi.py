"""
Halaman Hasil Segmentasi
===========================
Menampilkan ringkasan segmentasi tiap cluster (label, prioritas, tindakan),
tabel ringkasan segmentasi, grafik distribusi prioritas penagihan, serta
tabel detail data hasil segmentasi.

Teks segmentasi & rekomendasi tindakan SAMSAT mengikuti notebook final
"FCM17.ipynb" (bagian 4.9 Segmentasi Risiko).
"""

import matplotlib.pyplot as plt
import streamlit as st


def tampilkan():
    st.markdown('<div class="page-title">Hasil Segmentasi</div>', unsafe_allow_html=True)

    if st.session_state.hasil_fcm is None:
        st.warning("Silakan upload dan proses dataset terlebih dahulu.")
        return

    df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik, distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi = st.session_state.hasil_fcm

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Cluster 0</div>
            <p><b>Segmentasi:</b> Segmen Risiko Durasi Tunggakan Tinggi</p>
            <p><b>Prioritas:</b> Sedang</p>
            <p><b>Tindakan:</b> Validasi dan pemutakhiran data wajib pajak, penelusuran alamat,
            serta sosialisasi kewajiban pembayaran Pajak Kendaraan Bermotor.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Cluster 1</div>
            <p><b>Segmentasi:</b> Segmen Risiko Nominal Tunggakan Tinggi</p>
            <p><b>Prioritas:</b> Tinggi</p>
            <p><b>Tindakan:</b> Prioritas penagihan, pemberitahuan berkala, dan informasi program
            keringanan/pemutihan pajak bagi wajib pajak dengan nominal tunggakan tinggi.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="card-title">Ringkasan Hasil Segmentasi Risiko</div>', unsafe_allow_html=True)
        st.dataframe(ringkasan_segmentasi, use_container_width=True)

    with st.container(border=True):
        st.markdown('<div class="card-title">Distribusi Prioritas Penagihan</div>', unsafe_allow_html=True)

        prioritas = df["PRIORITAS"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(prioritas.index, prioritas.values, color="#0b3c82")
        ax.set_title("Distribusi Prioritas Penagihan")
        ax.set_xlabel("Kategori")
        ax.set_ylabel("Jumlah Wajib Pajak")

        for i, v in enumerate(prioritas.values):
            ax.text(i, v, str(v), ha="center", va="bottom")

        st.pyplot(fig)

    with st.container(border=True):
        st.markdown('<div class="card-title">Data Hasil Segmentasi</div>', unsafe_allow_html=True)

        st.dataframe(
            df[
                [
                    "LAMA MENUNGGAK",
                    "LAMA_HARI",
                    "TOTAL TUNGGAKAN",
                    "CLUSTER",
                    "SEGMENTASI",
                    "PRIORITAS",
                    "TINDAKAN_SAMSAT"
                ]
            ],
            use_container_width=True
        )
