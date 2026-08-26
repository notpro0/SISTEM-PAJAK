"""
Modul excel_export.py
========================
Berisi fungsi untuk menyusun file Excel hasil analisis
(multi-sheet) yang siap diunduh pengguna.

Struktur sheet mengikuti notebook final "FCM17.ipynb":
sheet dasar (Hasil Segmentasi, Evaluasi FPC, Centroid, Karakteristik
Cluster, Distribusi Cluster) ditambah sheet "Cluster 0" dan "Cluster 1"
yang berisi data tiap cluster secara terpisah, diurutkan dari Lama
Menunggak (LAMA_HARI) terlama ke tersingkat.
"""

import io

import pandas as pd


def buat_excel_hasil(
    df,
    df_fpc,
    centroid_df,
    karakteristik,
    distribusi,
    ringkasan_karakteristik=None,
):
    """
    Menyusun workbook Excel dengan sheet:
    - Hasil Segmentasi (seluruh data)
    - Evaluasi FPC
    - Centroid
    - Ringkasan Karakteristik (nilai asli, opsional)
    - Karakteristik Cluster (statistik lengkap)
    - Distribusi Cluster
    - Cluster 0 (data cluster 0 saja, diurutkan LAMA_HARI terlama)
    - Cluster 1 (data cluster 1 saja, diurutkan LAMA_HARI terlama)

    Mengembalikan bytes file Excel (siap dipakai st.download_button).
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Hasil Segmentasi")
        df_fpc.to_excel(writer, index=False, sheet_name="Evaluasi FPC")
        centroid_df.to_excel(writer, index=False, sheet_name="Centroid")

        if ringkasan_karakteristik is not None:
            ringkasan_karakteristik.to_excel(writer, sheet_name="Ringkasan Karakteristik")

        karakteristik.to_excel(writer, sheet_name="Karakteristik Cluster")
        distribusi.to_excel(writer, index=False, sheet_name="Distribusi Cluster")

        if "CLUSTER" in df.columns and "LAMA_HARI" in df.columns:
            for c in sorted(df["CLUSTER"].unique()):
                data_cluster = (
                    df[df["CLUSTER"] == c]
                    .sort_values(by="LAMA_HARI", ascending=False)
                    .reset_index(drop=True)
                )
                data_cluster.to_excel(writer, index=False, sheet_name=f"Cluster {c}")

    return output.getvalue()
