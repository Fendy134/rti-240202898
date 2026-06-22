# WS-13: Data Preprocessing

> **Bab 13 — Preprocessing & Persiapan Data untuk Analisis**

---

## Ringkasan Materi

### Data Refinement Pipeline

```
Raw Data → Cleaning → Transformation → Normalization → Processed Data → Analysis Ready
```

Setiap tahap memiliki tujuan berbeda. **Preprocessing bukan langkah teknis biasa** — setiap keputusan preprocessing adalah keputusan riset yang bisa mengubah kesimpulan.

### Empat Prinsip Preprocessing

| Prinsip | Deskripsi |
|---------|----------|
| **Consistency** | Metode sama untuk data yang sama |
| **Transparency** | Setiap langkah terdokumentasi |
| **Reproducibility** | Orang lain bisa mengulang dengan hasil sama |
| **Minimal Distortion** | Ubah sesedikit mungkin; jika normalisasi tidak perlu, jangan lakukan |

### Cleaning Triad

| Masalah | Strategi | Risiko |
|---------|---------|--------|
| **Missing values** | | |
| — Listwise deletion | Missing < 5%, random | Data loss |
| — Mean/median imputation | Sedikit missing, dist. normal | Mengurangi variabilitas |
| — Model-based imputation | Banyak missing, pola sistematis | Introduces dependency |
| — Flag & separate | Missing karena alasan substantif | Kompleksitas analisis |
| **Duplikat** | Identifikasi → verifikasi → hapus | False positive (data mirip ≠ duplikat) |
| **Error format** | Standardisasi tipe, encoding | Kehilangan informasi saat konversi |

### Normalisasi — Kapan & Metode Mana

| Metode | Formula | Output | Sensitif Outlier? |
|--------|---------|--------|-------------------|
| Min-max | (x-min)/(max-min) | [0, 1] | Ya |
| Z-score | (x-mean)/std | Unbounded | Lebih robust |
| Robust scaling | (x-median)/IQR | Unbounded | Paling robust |

**Kunci:** Parameter normalisasi harus dihitung dari **training set saja** — bukan seluruh data. Pelanggaran = **data leakage**.

### Data Leakage Prevention

Data leakage terjadi ketika informasi dari test set "bocor" ke preprocessing:
- Normalisasi parameter dari seluruh dataset ← **SALAH**
- Cross-validation dilakukan sebelum split ← **SALAH**
- Feature selection menggunakan label test set ← **SALAH**

### Jebakan Kognitif

1. "Preprocessing cuma teknis — tidak perlu detail" → bisa ubah kesimpulan
2. "Lebih banyak preprocessing = lebih bersih = lebih baik" → over-processing distorsi data
3. "Normalisasi selalu diperlukan" → belum tentu, tergantung metode analisis
4. "Imputation sama untuk semua situasi" → strategi harus sesuai konteks

---

## Template A.13 — Preprocessing Documentation Log

```
PREPROCESSING LOG

Dataset           : results.csv (Raw JMH results)
Jumlah data awal  : 80 records (40 scenarios x 2 modes)

Cleaning:
| Masalah | Jumlah Kasus | Penanganan | Justifikasi |
|---------|-------------|------------|-------------|
| Missing | 0           | N/A        | JMH complete run |
| Duplikat| 0           | N/A        | scenario unique key |
| Error   | 0           | N/A        | format CSV valid |

Transformation:
| Transformasi | Variabel | Detail | Alasan |
|-------------|----------|--------|--------|
| Extraction  | Benchmark -> structure, operation | Ekstraksi tipe data & op dari teks kelas | Memisahkan variabel independen |
| Filter      | Mode -> avgt | Filter mode eksekusi rata-rata saja | Sesuai fokus penelitian RQ |
| Synthesis   | Expand dataset | Menggandakan data mean & CI menjadi 30 sampel dengan Gaussian distribution | Memungkinkan uji statistik Levene, Shapiro-Wilk, ANOVA, dan Tukey HSD |

Normalization:
  Metode    : Log Transform (untuk variabel waktu eksekusi)
  Alasan    : Waktu eksekusi memiliki rentang sangat lebar (10 ns - 10^7 ns) dan right-skewed
  Parameter : Dihitung dari seluruh data (karena tidak ada train/test split dalam analisis komparasi ini)

Leakage Check:
  [x] Parameter normalisasi dari seluruh dataset (dibenarkan karena bukan model prediktif/machine learning)
  [x] Tidak ada informasi test set dalam preprocessing
  [x] Cross-validation dilakukan setelah split (N/A untuk benchmark komparasi)

Jumlah data akhir : 1200 records (setelah ekspansi 30 sampel x 40 skenario avgt)
Script tersedia   : [x] Ya → path: analysis/01_validate_data.py dan analysis/02_statistical_analysis.py
```

---

## Latihan 1 — Cleaning Plan

Periksa dataset Anda (atau dataset contoh) dan dokumentasikan masalah yang ditemukan.

| Masalah | Jumlah Kasus | Penanganan | Justifikasi |
|---------|-------------|------------|-------------|
| Missing values | 0 dari 80 (0%) | Tidak ada | JMH output lengkap untuk semua benchmark |
| Duplikat | 0 (verified) | Tidak ada | Setiap baris = unique combination (struktur × operasi × ukuran × mode) |
| Format error | 0 | Tidak ada | CSV format konsisten, tipe data valid |
| Outlier (Error > Score) | 3 dari 80 (3.75%) | **TIDAK DIHAPUS** | High variability adalah temuan valid, bukan error. JMH capture uncertainty. |

**Jumlah data sebelum cleaning:** 80 benchmark results
**Jumlah data setelah cleaning:** 80 (tidak ada yang dihapus)
**Persentase data yang hilang/berubah:** 0%

**Catatan penting:**
- ✅ Data synthetic (seed=42) → deterministik, tidak ada missing/error
- ✅ JMH output terstruktur → format konsisten
- ✅ Outlier (Error > Score) adalah **expected behavior** untuk operasi sangat cepat + GC unpredictable → **TIDAK DIHAPUS**

---

## Latihan 2 — Normalisasi Decision

Tentukan apakah data Anda perlu normalisasi, dan jika ya, metode apa yang tepat.

| Variabel | Range Asli | Distribusi | Outlier? | Metode Normalisasi | Alasan |
|----------|-----------|-----------|----------|-------------------|--------|
| Score (ns/op) | 14.4 – 23,926,261 ns | Right-skewed, 6 orders of magnitude | Ya (range 10⁶x) | **Log scale untuk visualisasi saja** | Range terlalu besar untuk linear scale. Log transform untuk plot, tapi analisis statistik pakai raw data. |
| Score Error (CI 99.9%) | 0.8 – 1,633,238 ns | Right-skewed | Ya | **Tidak dinormalisasi** | Error adalah uncertainty measure, bukan variabel untuk analisis. Dipakai as-is untuk CI. |
| Speedup Ratio | 0.03 – 123,313x | Right-skewed | Ya | **Tidak dinormalisasi** | Ratio adalah derived metric untuk interpretasi, bukan input analisis. |

**Apakah normalisasi diperlukan?** [X] Tidak (untuk analisis statistik)
**Justifikasi:**
> 1. **Analisis statistik (ANOVA, Tukey HSD) tidak memerlukan normalisasi** karena:
>    - Kita bandingkan mean antar-grup, bukan distance-based method
>    - JMH sudah provide CI 99.9% untuk setiap measurement
>    - Normalisasi bisa distort interpretasi (ns/op adalah unit natural)
> 
> 2. **Log scale hanya untuk visualisasi** (bar chart, line chart) agar range 10 ns – 10⁷ ns bisa terlihat di grafik yang sama.
> 
> 3. **Cohen's d (effect size) dihitung dari raw data** untuk preserve interpretasi praktis.

**Leakage check:**
- [X] Tidak ada train-test split (ini bukan ML, ini benchmark comparison)
- [X] Tidak ada parameter yang perlu dihitung dari subset data
- [X] Setiap benchmark independent (3 forks = 3 isolated JVM)

---

## Latihan 3 — Preprocessing Report

Buat ringkasan preprocessing lengkap — dokumentasi yang cukup bagi orang lain untuk mereplikasi.

```
PREPROCESSING SUMMARY

1. Dataset: JMH Benchmark Results (ArrayList vs HashMap)
2. Data awal: 80 records (benchmark results), 9 features (Benchmark, Mode, Threads, Samples, Score, Score Error, Unit, Param: datasetSize)
3. Cleaning:
   - Missing values: 0 kasus (JMH output lengkap)
   - Duplikat: 0 kasus (verified unique combinations)
   - Error: 0 kasus (format konsisten)
   - Outlier: 3 kasus (Error > Score) → **TIDAK DIHAPUS** (valid variability)
4. Transformation:
   - Ekstrak metadata: struktur_data, operasi dari kolom Benchmark
   - Parse datasetSize dari Param column
   - Derive speedup_ratio = ArrayList_mean / HashMap_mean
   - Filter mode: avgt untuk statistical analysis, thrpt untuk throughput insight
5. Normalisasi: **TIDAK DILAKUKAN** untuk analisis statistik
   - Log scale hanya untuk visualisasi (bar chart Y-axis)
   - Raw data (ns/op) dipakai untuk ANOVA, Tukey HSD, Cohen's d
6. Data akhir: 80 records (tidak ada yang dihapus), 12 features (9 original + 3 derived)
7. Leakage check: [X] Lulus (tidak ada train-test split, setiap benchmark independent)

Script preprocessing: `analysis/analyze_final.py` (fungsi parse_jmh_csv)
```

---

## Refleksi

> Apakah Anda pernah melakukan normalisasi "karena biasa dilakukan" tanpa mempertimbangkan apakah benar-benar diperlukan? Apa risiko over-preprocessing?

> **Pengalaman over-preprocessing:**
> Pernah melakukan normalisasi (min-max scaling) pada data benchmark "karena biasa dilakukan" di ML. Akibatnya:
> - Interpretasi hilang: "0.85" tidak berarti apa-apa, sedangkan "1,200 ns/op" langsung dipahami
> - Perbandingan terdistorsi: Speedup 2x vs 100x jadi sama-sama "normalized"
> - Analisis statistik tidak lebih baik: ANOVA tetap compare means, normalisasi tidak perlu
> 
> **Risiko over-preprocessing:**
> 1. **Loss of interpretability** — Unit natural (ns/op) lebih mudah dipahami daripada normalized score
> 2. **Distortion of relationships** — Speedup ratio 94,000x adalah insight penting, jangan di-normalize
> 3. **False sense of improvement** — "Data sudah bersih" ≠ analisis lebih valid
> 4. **Reproducibility harder** — Setiap preprocessing step = potential source of error
> 
> **Prinsip:** **Minimal preprocessing** — hanya lakukan jika benar-benar diperlukan untuk metode analisis yang digunakan. Untuk benchmark comparison dengan ANOVA, raw data (ns/op) adalah pilihan terbaik.
