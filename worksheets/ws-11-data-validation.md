# WS-11: Data Validation & Integrity

> **Bab 11 — Validasi Data & Integritas**

---

## Ringkasan Materi

### Data Trust Model

```
Raw Data → Data Cleaning → Consistency Check → Validation Process → Trusted Data
```

Data mentah belum bisa dipercaya. Harus melewati pipeline validasi sebelum siap untuk analisis statistik.

### Empat Pilar Data Quality

| Pilar | Deskripsi | Contoh Pelanggaran |
|-------|----------|-------------------|
| **Accuracy** | Nilai dalam range masuk akal | Akurasi = 1.5 (di luar [0,1]) |
| **Consistency** | Format seragam di semua run | Run 1: CSV, Run 2: JSON |
| **Completeness** | Tidak ada data hilang dari plan | 97 dari 100 run tercatat |
| **Validity** | Data sesuai desain eksperimen | Parameter baseline tercampur treatment |

### Proses Validasi Progresif

1. **Format validation** — Tipe file, header, kolom
2. **Range validation** — Nilai dalam batas logis
3. **Consistency validation** — Format seragam antar-run
4. **Logic validation** — Data cocok dengan desain eksperimen

Jika gagal di langkah awal → tidak perlu lanjut.

### Anomaly Detection — 3 Jenis

| Jenis | Deskripsi | Deteksi |
|-------|----------|---------|
| **Statistical outlier** | Nilai di luar distribusi normal | IQR: < Q1-1.5×IQR atau > Q3+1.5×IQR |
| **Contextual anomaly** | Normal absolut, abnormal dalam konteks | Run 1-10: ~91%, Run 11-20: ~88% |
| **Pattern anomaly** | Pola sistematis (bukan random) | Performa menurun berurutan |

**Prinsip:** Detect → Investigate → Document → Decide — **JANGAN langsung hapus.**

### Engineering vs Research Validation

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Tujuan | Data sesuai spesifikasi bisnis | Data layak untuk analisis statistik |
| Missing data | Impute / set default | Investigasi penyebab → dokumentasi |
| Outlier | Bug → fix | Mungkin temuan → investigasi |
| Dokumentasi | Minimal (log error) | Komprehensif (anomali + keputusan) |

### Jebakan Kognitif

1. "Logging otomatis ≠ data benar" → bisa ada bug di logger
2. "Outlier = hapus" → bisa jadi temuan penting
3. "Dataset kecil tidak perlu validasi" → justru lebih rentan
4. "Mean normal = data benar" → [94, 95, 93, **44**, 94] → mean 84% terlihat wajar

---

## Template A.11 — Data Validation Checklist

```
DATA VALIDATION CHECKLIST

Completeness:
  [x] Semua skenario tercakup
  [x] Jumlah run sesuai rencana
  [x] Tidak ada file output hilang
  Missing: 0 dari 80 data points (40 scenarios x 2 modes)

Format Consistency:
  [x] Semua file format sama (CSV/JSON/...)
  [x] Header konsisten
  [x] Tipe data konsisten (numerik tetap numerik)

Range & Logic:
  [x] Nilai dalam range masuk akal (Score > 0, Samples = 30)
  [x] Tidak ada waktu negatif
  [x] Metrik 0–100%, tidak di luar range (N/A untuk execution time)
  Anomali ditemukan: 3 skenario memiliki Error > Score karena operasi mikro-ns sangat cepat

Cross-Validation:
  [x] Run identik → hasil mendekati
  [x] Trend konsisten dengan ekspektasi teori (HashMap O(1) vs ArrayList O(N))

Keputusan:
  [x] Data siap analisis
  [ ] Perlu cleaning
  [ ] Perlu re-run (skenario: N/A)
```

---

## Latihan 1 — Completeness Check

Verifikasi apakah semua data yang direncanakan sudah terkumpul.

| Skenario | Run Direncanakan | Run Tercatat | Missing | Alasan |
|----------|-----------------|-------------|---------|--------|
| ArrayList × 5 ops × 4 sizes × 2 modes | 40 | 40 | 0 |  Complete |
| HashMap × 5 ops × 4 sizes × 2 modes | 40 | 40 | 0 |  Complete |
| Total samples per benchmark | 30 (3 forks × 10 iter) | 30 | 0 |  Complete |

**Total expected:** 80 benchmark results (40 × 2 modes) | **Total actual:** 80 | **Missing:** 0

**Keputusan untuk data missing:**
>  Tidak ada data missing. Semua 40 kombinasi (2 struktur × 5 operasi × 4 ukuran) ter-record untuk kedua mode (avgt + thrpt).
>  Setiap benchmark punya 30 samples dari 3 forks × 10 measurement iterations.
>  File `results.csv` berisi 80 baris + 1 header = 81 baris total.

---

## Latihan 2 — Anomaly Investigation

Periksa data Anda untuk anomali. Gunakan metode IQR atau z-score.

**Dataset sampel: ArrayList.delete @ 1000 elements (avgt mode)**

| Fork | Score (ns/op) | Score Error (99.9%) |
|------|---------------|---------------------|
| 1 | 19,410.99 | 64,460.79 |

**Deteksi anomali:**
- Score: 19,410.99 ns/op
- Error: 64,460.79 ns/op (332% dari score!)
- **Anomali:** Error > Score → CI sangat lebar

**Investigasi:**

| Anomali | Nilai | Kemungkinan Penyebab | Keputusan |
|---------|-------|---------------------|-----------|
| ArrayList.delete @ 1K | Error 64,460 > Score 19,410 | JMH capture high variability karena operasi sangat cepat (~19μs) + GC unpredictable |  **VALID** — JMH designed untuk capture variability. CI lebar = uncertainty tinggi, bukan bug. Lapor apa adanya. |
| ArrayList.insert @ 1M | Score 1,932 ns, Error 6,970 ns | Variability tinggi karena array resize unpredictable di 10⁶ elements |  **VALID** — Dokumentasi: "High variability due to dynamic array resizing" |
| HashMap.insert @ 10K | Score 3,254 ns, Error 9,707 ns | Hash collision + rehashing di load factor > 0.75 |  **VALID** — Expected behavior untuk HashMap growth |

---

## Latihan 3 — Validation Report

Buat laporan validasi ringkas untuk dataset eksperimen Anda.

**1. Completeness:** 100% data terkumpul (80/80 benchmark results)

**2. Format:** [X] Konsisten
-  Semua data dalam CSV format
-  Header konsisten: "Benchmark","Mode","Threads","Samples","Score","Score Error (99.9%)","Unit","Param: datasetSize"
-  Tipe data konsisten: Score & Error = double, Samples = int

**3. Range check (anomali):**
-  Semua Score > 0 (valid)
-  Semua Samples = 30 (3 forks × 10 iterations)
-  Threads = 1 (single-threaded sesuai design)
-  3 benchmark dengan Error > Score (high variability, tapi VALID karena JMH capture uncertainty)

**4. Logic check:** [X] Parameter sesuai plan
-  Dataset sizes: 1000, 10000, 100000, 1000000 (sesuai @Param)
-  Modes: avgt + thrpt (sesuai @BenchmarkMode)
-  JVM flags: -Xms4g -Xmx4g -XX:+UseG1GC (sesuai pom.xml)
-  Seed: 42 (DatasetGenerator)

**Kesimpulan:** [X] Data siap analisis
-  Completeness: 100%
-  Consistency: Format seragam
-  Validity: Sesuai desain eksperimen
-  Representativeness: 30 samples per benchmark cukup untuk statistical testing
-  High variability di beberapa benchmark (Error > Score) adalah **expected behavior** untuk operasi sangat cepat + GC unpredictable → lapor dengan CI 99.9%

---

## Refleksi

> Apa perbedaan antara "data yang benar" dan "data yang dipercaya"? Mengapa proses validasi formal diperlukan meskipun data dikumpulkan secara otomatis?

> **"Data yang benar"** = data sesuai spesifikasi teknis (format CSV, kolom lengkap, tipe data match).
> 
> **"Data yang dipercaya"** = data yang sudah melewati validasi formal (completeness, consistency, range check, logic check) dan siap untuk analisis statistik.
> 
> **Mengapa validasi formal diperlukan meskipun data dikumpulkan otomatis?**
> 1. **Logger bisa punya bug** — JMH mature tapi tetap perlu verify output
> 2. **Anomali bisa jadi temuan** — Error > Score bukan bug, tapi insight tentang variability
> 3. **Completeness tidak guaranteed** — Bisa ada run yang crash/timeout
> 4. **Consistency perlu dicek** — Format bisa berubah antar-version
> 5. **Trust = reproducibility** — Validasi formal adalah bukti bahwa data reliable
> 
> **Kesimpulan:** Validasi formal mengubah "data mentah" menjadi "trusted dataset" yang layak untuk klaim ilmiah.
