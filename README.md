# SAMSAT PKB Analytics

Dashboard Streamlit untuk analisis dan segmentasi risiko tunggakan Pajak Kendaraan
Bermotor (PKB) menggunakan metode **Fuzzy C-Means (FCM)**.

## Struktur Proyek

```
SAMSAT_PKB_ANALYTICS/
│
├── app.py                     # File utama (konfigurasi, routing menu)
│
├── assets/
│   ├── style.css               # Seluruh styling dashboard
│   └── logo.png                 # (opsional, belum dipakai di kode)
│
├── pages/
│   ├── beranda.py               # Halaman Beranda (KPI ringkas, alur sistem)
│   ├── upload.py                 # Upload dataset & trigger proses FCM
│   ├── analisis_fcm.py           # KPI, evaluasi FPC, tabel centroid
│   ├── visualisasi.py            # Scatter plot, boxplot, histogram, dsb.
│   ├── karakteristik.py          # Statistik deskriptif & distribusi per cluster
│   ├── segmentasi.py             # Ringkasan segmentasi & tabel hasil
│   └── download.py               # Tombol download Excel hasil analisis
│
├── utils/
│   ├── preprocessing.py          # Konversi & normalisasi data mentah
│   ├── clustering.py             # Pipeline Fuzzy C-Means & segmentasi
│   ├── excel_export.py           # Penyusunan file Excel multi-sheet
│   ├── formatter.py              # Format rupiah & angka
│   └── helper.py                 # Load CSS, sidebar, session_state
│
├── data/                        # (kosong, untuk data upload user jika diperlukan)
├── output/                      # (kosong, untuk cache hasil export jika diperlukan)
│
├── requirements.txt
└── README.md
```

## Cara Menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Alur Sistem

1. **Upload Dataset** — user mengunggah file Excel (`.xlsx`) berisi kolom wajib:
   `LAMA MENUNGGAK`, `POKOK`, `DENDA`, `TOTAL TUNGGAKAN`.
2. **Transformasi Data** — kolom `LAMA MENUNGGAK` (teks, mis. "1 tahun 2 bulan")
   dikonversi menjadi `LAMA_HARI` (angka hari).
3. **Normalisasi** — `LAMA_HARI` dan `TOTAL TUNGGAKAN` dinormalisasi dengan `MinMaxScaler`.
4. **Fuzzy C-Means** — dijalankan untuk kandidat jumlah cluster 2–5.
5. **Evaluasi FPC** — jumlah cluster dengan nilai *Fuzzy Partition Coefficient* tertinggi dipilih sebagai cluster optimal.
6. **Visualisasi & Segmentasi** — hasil clustering divisualisasikan dan diberi label
   segmentasi risiko + rekomendasi tindakan SAMSAT.
7. **Download Excel** — seluruh hasil (data, evaluasi FPC, centroid, karakteristik,
   distribusi) diekspor ke satu file Excel multi-sheet.

## Navigasi sidebar

Folder `pages/` biasanya membuat Streamlit otomatis menampilkan menu navigasi
bawaan di atas sidebar. Ini sudah dinonaktifkan lewat `.streamlit/config.toml`
(`showSidebarNavigation = false`), sehingga yang tampil hanya menu radio
kustom "MENU UTAMA" dari `utils/helper.py`. Pastikan folder `.streamlit/`
ikut ter-copy saat deploy / dijalankan.
