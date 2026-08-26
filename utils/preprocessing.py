"""
Modul preprocessing.py
========================
Berisi fungsi-fungsi untuk membersihkan, mengonversi, dan
menormalisasi data mentah SAMSAT sebelum masuk ke tahap clustering
Fuzzy C-Means.

Disesuaikan dengan notebook "Proses_FCM.ipynb":
- TOTAL TUNGGAKAN selalu dihitung ulang sebagai POKOK + DENDA
  (bukan diambil mentah-mentah dari kolom upload), supaya konsisten
  dengan data asli.
"""

import re

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

KOLOM_WAJIB = ["LAMA MENUNGGAK", "POKOK", "DENDA"]
KOLOM_KORELASI = ["LAMA_HARI", "POKOK", "DENDA", "TOTAL TUNGGAKAN"]


def konversi_lama_menunggak(teks):
    """
    Mengonversi teks lama menunggak (contoh: "1 tahun 2 bulan 5 hari")
    menjadi total hari (integer).
    """
    if pd.isna(teks):
        return np.nan

    teks = str(teks).lower()

    tahun = re.search(r"(\d+)\s*tahun", teks)
    bulan = re.search(r"(\d+)\s*bulan", teks)
    hari = re.search(r"(\d+)\s*hari", teks)

    tahun = int(tahun.group(1)) if tahun else 0
    bulan = int(bulan.group(1)) if bulan else 0
    hari = int(hari.group(1)) if hari else 0

    return (tahun * 365) + (bulan * 30) + hari


def cek_data_kosong_dan_duplikat(df_awal):
    """
    Mengecek jumlah missing value per kolom dan jumlah baris duplikat,
    sesuai tahap 4.3.1 Data Cleaning pada notebook.
    """
    missing = df_awal.isnull().sum()
    jumlah_duplikat = int(df_awal.duplicated().sum())

    return missing, jumlah_duplikat


def bersihkan_dan_normalisasi(df_awal):
    """
    Membersihkan kolom numerik, mengonversi kolom LAMA MENUNGGAK
    menjadi LAMA_HARI, menghitung ulang TOTAL TUNGGAKAN = POKOK + DENDA,
    menghapus baris kosong, lalu menormalisasi kolom LAMA_HARI dan
    TOTAL TUNGGAKAN menggunakan MinMaxScaler.

    Mengembalikan dataframe yang sudah bersih dan siap dipakai
    untuk proses Fuzzy C-Means.
    """
    df = df_awal.copy()

    df["POKOK"] = pd.to_numeric(df["POKOK"], errors="coerce")
    df["DENDA"] = pd.to_numeric(df["DENDA"], errors="coerce")

    # TOTAL TUNGGAKAN selalu dihitung ulang dari POKOK + DENDA
    # (mengikuti langkah "MEMASTIKAN DATA ASLI TETAP" pada notebook),
    # bukan memakai kolom TOTAL TUNGGAKAN mentah dari file upload.
    df["TOTAL TUNGGAKAN"] = df["POKOK"] + df["DENDA"]

    df["LAMA_HARI"] = df["LAMA MENUNGGAK"].apply(konversi_lama_menunggak)

    df = df.dropna(subset=["LAMA_HARI", "TOTAL TUNGGAKAN"])

    scaler = MinMaxScaler()
    hasil_norm = scaler.fit_transform(df[["LAMA_HARI", "TOTAL TUNGGAKAN"]])

    df["LAMA_HARI_NORMALISASI"] = hasil_norm[:, 0]
    df["TOTAL_TUNGGAKAN_NORMALISASI"] = hasil_norm[:, 1]

    return df


def hitung_korelasi(df):
    """
    Menghitung matriks korelasi Pearson antara LAMA_HARI, POKOK, DENDA,
    dan TOTAL TUNGGAKAN, sesuai tahap 4.2.2 Uji Korelasi Pearson pada notebook.
    """
    kolom_tersedia = [k for k in KOLOM_KORELASI if k in df.columns]
    return df[kolom_tersedia].corr(method="pearson")


def kolom_wajib_lengkap(df_awal, kolom_wajib=None):
    """
    Mengecek apakah dataframe memiliki seluruh kolom wajib.
    TOTAL TUNGGAKAN tidak wajib ada di file upload karena akan
    dihitung ulang otomatis dari POKOK + DENDA.
    """
    if kolom_wajib is None:
        kolom_wajib = KOLOM_WAJIB

    return all(kolom in df_awal.columns for kolom in kolom_wajib)
