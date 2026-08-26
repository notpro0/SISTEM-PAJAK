"""
Modul clustering.py
======================
Berisi seluruh logika inti Fuzzy C-Means (FCM):
- evaluasi FPC untuk beberapa jumlah cluster (2-5, sebagai perbandingan)
- clustering final dengan jumlah cluster TETAP = 2
- pelabelan segmentasi & rekomendasi tindakan SAMSAT
- karakteristik kendaraan per cluster (Merk, Jenis, Tipe, Tahun Kendaraan)

Fungsi utama yang dipanggil dari halaman Upload adalah proses_data_fcm().

Catatan penyesuaian dengan notebook "Proses_FCM.ipynb":
Notebook menjalankan evaluasi FPC untuk c = 2, 3, 4, 5 hanya sebagai
perbandingan/laporan, tetapi clustering FINAL yang dipakai untuk
segmentasi selalu memakai c = 2 (JUMLAH_CLUSTER_FINAL). Mapping
SEGMENTASI/PRIORITAS/TINDAKAN_SAMSAT juga hanya didefinisikan untuk
2 cluster (cluster 0 dan cluster 1), jadi jumlah cluster TIDAK dipilih
otomatis dari nilai FPC tertinggi.
"""

import numpy as np
import pandas as pd
import skfuzzy as fuzz

from utils.preprocessing import bersihkan_dan_normalisasi

KOLOM_NORMALISASI = ["LAMA_HARI_NORMALISASI", "TOTAL_TUNGGAKAN_NORMALISASI"]

# Jumlah cluster final yang dipakai untuk segmentasi (mengikuti notebook).
JUMLAH_CLUSTER_FINAL = 2

# Seed tetap agar hasil Fuzzy C-Means konsisten (reproducible) setiap kali
# dataset diproses ulang. Tanpa seed tetap, inisialisasi FCM bersifat acak
# sehingga hasil cluster bisa sedikit berbeda tiap kali tombol "Proses
# Dataset" ditekan meski datanya sama persis.
SEED_FCM = 42

# Kolom kategori kendaraan yang dianalisis per cluster, jika tersedia
# di dataset (kolom bersifat opsional; dilewati kalau tidak ada).
#
# Setiap kategori punya daftar alias nama kolom, diurutkan dari yang
# paling mungkin dipakai. Kolom "MERK" adalah nama resmi terbaru untuk
# Merk Kendaraan (sebelumnya sempat terbaca sebagai "Column 1" saat
# header di file Excel kosong/tidak diberi nama) - keduanya tetap
# didukung supaya tetap kompatibel dengan file lama.
DAFTAR_KATEGORI_KENDARAAN = [
    {"label": "Merk Kendaraan", "alias": ["MERK", "Merk", "MEREK", "Column 1"]},
    {"label": "Jenis Kendaraan", "alias": ["TIPE", "Tipe"]},
    {"label": "Tipe Kendaraan", "alias": ["MODEL", "Model"]},
]


def evaluasi_konvergensi(data_fcm, daftar_cluster=(2, 3, 4, 5)):
    """
    Menjalankan Fuzzy C-Means untuk beberapa kandidat jumlah cluster dan
    mencatat proses konvergensinya (nilai fungsi objektif J pada iterasi
    pertama & terakhir, serta jumlah iterasi sampai konvergen), sesuai
    tabel "HASIL PENGUJIAN KONVERGENSI FCM" pada notebook.
    """
    hasil = []

    for c in daftar_cluster:
        _, _, _, _, jm, _, _ = fuzz.cluster.cmeans(
            data_fcm,
            c=c,
            m=2,
            error=0.005,
            maxiter=1000,
            init=None,
            seed=SEED_FCM
        )

        hasil.append({
            "No": len(hasil) + 1,
            "Skenario": f"C = {c}",
            "J Iterasi 1": round(jm[0], 4),
            "J Iterasi Final": round(jm[-1], 4),
            "Iterasi Konvergen": len(jm),
        })

    tabel = pd.DataFrame(hasil)

    iterasi_min = tabel["Iterasi Konvergen"].min()
    iterasi_max = tabel["Iterasi Konvergen"].max()

    tabel["Keterangan"] = tabel["Iterasi Konvergen"].apply(
        lambda x: "Konvergen tercepat" if x == iterasi_min
        else "Konvergen terlama" if x == iterasi_max
        else "-"
    )

    return tabel


def evaluasi_fpc(data_fcm, daftar_cluster=(2, 3, 4, 5)):
    """
    Menjalankan Fuzzy C-Means untuk beberapa kandidat jumlah cluster
    dan mengembalikan dataframe nilai FPC (Fuzzy Partition Coefficient)
    untuk masing-masing jumlah cluster. Tabel ini hanya untuk perbandingan,
    BUKAN untuk memilih otomatis jumlah cluster final.
    """
    hasil_fpc = []

    for c in daftar_cluster:
        _, _, _, _, _, _, fpc = fuzz.cluster.cmeans(
            data_fcm,
            c=c,
            m=2,
            error=0.005,
            maxiter=1000,
            init=None,
            seed=SEED_FCM
        )

        hasil_fpc.append({
            "Jumlah Cluster": c,
            "FPC": fpc
        })

    return pd.DataFrame(hasil_fpc)


def jalankan_fcm(data_fcm, cluster_optimal):
    """
    Menjalankan Fuzzy C-Means final menggunakan jumlah cluster tertentu.
    Mengembalikan centroid (cntr), matriks keanggotaan (u), dan nilai FPC final.
    """
    cntr, u, _, _, _, _, fpc_final = fuzz.cluster.cmeans(
        data_fcm,
        c=cluster_optimal,
        m=2,
        error=0.005,
        maxiter=1000,
        init=None,
        seed=SEED_FCM
    )

    return cntr, u, fpc_final


def beri_label_segmentasi(df, centroid_df=None):
    """
    Memberi label segmentasi, prioritas, dan rekomendasi tindakan SAMSAT
    berdasarkan hasil cluster (khusus untuk 2 cluster: 0 dan 1).
    Teks label mengikuti notebook final "FCM17.ipynb".

    PENTING - kenapa mapping tidak boleh statis ke index cluster (0/1):
    Index cluster hasil Fuzzy C-Means (dari np.argmax(u, axis=0)) TIDAK
    selalu konsisten menunjuk ke karakteristik yang sama setiap kali data
    diproses. Kadang cluster "0" berisi data dengan nominal tunggakan
    tinggi, kadang justru cluster "1". Kalau label di-mapping langsung
    berdasarkan index (0 -> Sedang, 1 -> Tinggi), hasil label bisa
    TERBALIK dari karakteristik data aslinya (mis. cluster 0 ternyata
    berisi tunggakan nominal tinggi tapi malah diberi label "Sedang").

    Supaya sesuai dengan notebook, label ditentukan secara DINAMIS
    berdasarkan nilai centroid ternormalisasi tiap cluster:
    - Cluster dengan centroid TOTAL_TUNGGAKAN_NORMALISASI lebih besar
      -> "Segmen Risiko Nominal Tunggakan Tinggi" & Prioritas "Tinggi".
    - Cluster satunya (LAMA_HARI_NORMALISASI relatif lebih besar)
      -> "Segmen Risiko Durasi Tunggakan Tinggi" & Prioritas "Sedang".

    Kalau centroid_df tidak diberikan, fallback memakai rata-rata nilai
    ternormalisasi per cluster dari df itu sendiri (hasil tetap konsisten
    dengan karakteristik data, bukan index cluster).
    """
    if df["CLUSTER"].nunique() != 2:
        return df

    # Tentukan cluster mana yang punya rata-rata TOTAL_TUNGGAKAN_NORMALISASI
    # lebih tinggi -> itu yang jadi cluster "Nominal Tunggakan Tinggi".
    if centroid_df is not None and "TOTAL_TUNGGAKAN_NORMALISASI" in centroid_df.columns:
        acuan = centroid_df.set_index("CLUSTER")["TOTAL_TUNGGAKAN_NORMALISASI"]
    else:
        acuan = df.groupby("CLUSTER")["TOTAL_TUNGGAKAN_NORMALISASI"].mean()

    cluster_nominal_tinggi = acuan.idxmax()
    cluster_durasi_tinggi = acuan.idxmin()

    peta_segmentasi = {
        cluster_durasi_tinggi: "Segmen Risiko Durasi Tunggakan Tinggi",
        cluster_nominal_tinggi: "Segmen Risiko Nominal Tunggakan Tinggi",
    }

    peta_prioritas = {
        cluster_durasi_tinggi: "Sedang",
        cluster_nominal_tinggi: "Tinggi",
    }

    peta_tindakan = {
        cluster_durasi_tinggi: (
            "Validasi dan pemutakhiran data wajib pajak, penelusuran alamat, "
            "serta sosialisasi kewajiban pembayaran Pajak Kendaraan Bermotor"
        ),
        cluster_nominal_tinggi: (
            "Prioritas penagihan, pemberitahuan berkala, dan informasi program "
            "keringanan/pemutihan pajak bagi wajib pajak dengan nominal tunggakan tinggi"
        ),
    }

    df["SEGMENTASI"] = df["CLUSTER"].map(peta_segmentasi)
    df["PRIORITAS"] = df["CLUSTER"].map(peta_prioritas)
    df["TINDAKAN_SAMSAT"] = df["CLUSTER"].map(peta_tindakan)

    return df


def hitung_ringkasan_karakteristik(df):
    """
    Menghitung ringkasan karakteristik cluster memakai nilai asli (bukan
    normalisasi): jumlah data, rata-rata Lama Menunggak (hari), dan
    rata-rata Total Tunggakan (Rp) per cluster. Sesuai tabel
    "KARAKTERISTIK CLUSTER (NILAI ASLI)" pada notebook.
    """
    ringkasan = df.groupby("CLUSTER").agg(
        Jumlah_Data=("CLUSTER", "count"),
        Rata_rata_Lama_Menunggak_Hari=("LAMA_HARI", "mean"),
        Rata_rata_Total_Tunggakan_Rp=("TOTAL TUNGGAKAN", "mean"),
    ).round(0)

    return ringkasan


def hitung_karakteristik(df):
    """Menghitung statistik deskriptif lengkap (count, mean, min, max) per cluster."""
    return df.groupby("CLUSTER")[["LAMA_HARI", "TOTAL TUNGGAKAN"]].agg(
        ["count", "mean", "min", "max"]
    )


def hitung_distribusi(df):
    """Menghitung jumlah data dan persentase anggota tiap cluster."""
    distribusi = df["CLUSTER"].value_counts().sort_index().reset_index()
    distribusi.columns = ["Cluster", "Jumlah Data"]
    distribusi["Persentase"] = (
        distribusi["Jumlah Data"] / distribusi["Jumlah Data"].sum() * 100
    ).round(2)

    return distribusi


def kolom_kategori_tersedia(df):
    """
    Mengembalikan list [(nama_kolom_asli, label), ...] untuk kategori
    kendaraan yang benar-benar ada di dataframe (Merk, Jenis, Tipe, Tahun
    Kendaraan). Untuk tiap kategori, alias pertama yang ditemukan di
    dataframe yang dipakai (mis. "MERK" lebih diprioritaskan daripada
    "Column 1" kalau keduanya ada).
    """
    hasil = []

    for kategori in DAFTAR_KATEGORI_KENDARAAN:
        for kolom in kategori["alias"]:
            if kolom in df.columns:
                hasil.append((kolom, kategori["label"]))
                break

    return hasil


def hitung_karakteristik_kategori(df, kolom_kategori, top_n=10):
    """
    Menghitung jumlah & persentase data per cluster untuk satu kolom
    kategori kendaraan (mis. Merk, Jenis, Tipe, Tahun Kendaraan),
    sesuai analisis "Karakteristik Merk/Jenis/Tipe/Tahun Kendaraan"
    pada notebook.

    Mengembalikan dict {cluster: dataframe (Jumlah, Persentase)}.
    """
    rekap = (
        df.groupby(["CLUSTER", kolom_kategori])
        .size()
        .reset_index(name="Jumlah")
    )

    rekap["Persentase"] = (
        rekap.groupby("CLUSTER")["Jumlah"]
        .transform(lambda x: round(x / x.sum() * 100, 2))
    )

    hasil = {}
    for c in sorted(df["CLUSTER"].unique()):
        data_cluster = (
            rekap[rekap["CLUSTER"] == c]
            .sort_values("Jumlah", ascending=False)
            .drop(columns="CLUSTER")
            .reset_index(drop=True)
        )
        hasil[c] = data_cluster.head(top_n)

    return hasil


def hitung_ringkasan_segmentasi(df):
    """
    Menghitung ringkasan jumlah data per kombinasi Cluster + Segmentasi,
    sesuai tabel "RINGKASAN HASIL SEGMENTASI RISIKO" pada notebook.
    """
    if "SEGMENTASI" not in df.columns:
        return pd.DataFrame(columns=["CLUSTER", "SEGMENTASI", "Jumlah Data"])

    return (
        df.groupby(["CLUSTER", "SEGMENTASI"])
        .size()
        .reset_index(name="Jumlah Data")
    )


def proses_data_fcm(df_awal):
    """
    Fungsi orkestrasi utama: menjalankan seluruh pipeline
    preprocessing -> evaluasi FPC (perbandingan) -> FCM final (c=2) -> segmentasi.

    Mengembalikan tuple:
    (df, df_fpc, cluster_optimal, fpc_final, centroid_df, karakteristik,
     distribusi, u, ringkasan_karakteristik, tabel_konvergensi, ringkasan_segmentasi)
    """
    df = bersihkan_dan_normalisasi(df_awal)

    data_fcm = df[KOLOM_NORMALISASI].values.T

    # Evaluasi FPC untuk c = 2..5, ditampilkan sebagai perbandingan saja.
    df_fpc = evaluasi_fpc(data_fcm)

    # Evaluasi konvergensi (J iterasi 1 & final, jumlah iterasi) untuk c = 2..5.
    tabel_konvergensi = evaluasi_konvergensi(data_fcm)

    # Jumlah cluster final SELALU 2, mengikuti notebook & mapping segmentasi.
    cluster_optimal = JUMLAH_CLUSTER_FINAL

    cntr, u, fpc_final = jalankan_fcm(data_fcm, cluster_optimal)

    cluster = np.argmax(u, axis=0)
    df["CLUSTER"] = cluster

    for i in range(cluster_optimal):
        df[f"MEMBERSHIP_CLUSTER_{i}"] = u[i]

    centroid_df = pd.DataFrame(cntr, columns=KOLOM_NORMALISASI)
    centroid_df["CLUSTER"] = centroid_df.index

    karakteristik = hitung_karakteristik(df)
    ringkasan_karakteristik = hitung_ringkasan_karakteristik(df)
    distribusi = hitung_distribusi(df)

    df = beri_label_segmentasi(df, centroid_df)

    ringkasan_segmentasi = hitung_ringkasan_segmentasi(df)

    return (
        df,
        df_fpc,
        cluster_optimal,
        fpc_final,
        centroid_df,
        karakteristik,
        distribusi,
        u,
        ringkasan_karakteristik,
        tabel_konvergensi,
        ringkasan_segmentasi,
    )
