# WS-10: Experiment Execution & Data Collection

> **Bab 10 — Eksekusi Eksperimen & Pengumpulan Data**

---

## Ringkasan Materi

### Experiment Execution Pipeline

```
Design → Execution Plan → Controlled Execution → Data Collection → Data Logging → Dataset for Analysis
```

### Multiple Run = Non-Negotiable

Single run **tidak pernah cukup** untuk klaim ilmiah. Minimum 5-10 run per skenario dengan seed berbeda. Multiple run menghasilkan:
- Mean, std, confidence interval
- Distribusi hasil → uji statistik
- Variabilitas → error bar di grafik

### Execution Plan

Setiap eksperimen harus memiliki plan sebelum eksekusi:
- Daftar skenario
- Jumlah run per skenario
- Random seed per run (pre-determined!)
- Urutan eksekusi (randomisasi/counterbalancing)
- Pre-execution checklist

### Data Logging Komprehensif

Setiap run menghasilkan log terstruktur:
1. **Identitas** — Run ID, timestamp, skenario
2. **Konfigurasi** — Semua parameter, seed, code version
3. **Hasil** — Semua metrik, output detail
4. **Metadata** — Waktu eksekusi, resource usage, warning/error

Format: CSV/JSON/database — **bukan stdout yang di-copy-paste**.

### Engineering vs Research Execution

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Run | Sekali (deploy) | Multiple (min 5-10, seed berbeda) |
| Logging | Error log, access log | Semua parameter, metrik, metadata |
| Anomali | Bug → fix → redeploy | Investigasi → dokumentasi → analisis |
| Urutan | Tidak penting | Bisa bias — perlu randomisasi |

### Anomali = Dokumentasi, Bukan Hapus

Run gagal/anomali tidak boleh dihapus tanpa dokumentasi. Bisa jadi:
- **Bug** → fix & re-run (dokumentasikan!)
- **Batas kemampuan metode** → DNF = temuan
- **Data yang bias** jika hanya simpan run "berhasil"

### Jebakan Kognitif

1. "Satu angka cukup" → tanpa distribusi, tidak bisa diuji
2. "Seed tidak penting" → bahkan algoritma deterministik bisa dipengaruhi library stokastik
3. "Run gagal langsung hapus" → kehilangan temuan potensial
4. "Semua run harus hari ini" → thermal throttling, fatigue

---

## Template A.10 — Execution Plan & Data Log

```
EXECUTION PLAN

| Run # | Skenario | Seed | Parameter | Status | Waktu | Output File |
|-------|----------|------|-----------|--------|-------|-------------|
| 1     | ArrayList.delete | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 12:45 | results.csv |
| 2     | ArrayList.insert | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 12:50 | results.csv |
| 3     | ArrayList.iterate| 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 12:55 | results.csv |
| 4     | ArrayList.search | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:00 | results.csv |
| 5     | ArrayList.update | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:05 | results.csv |
| 6     | HashMap.delete   | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:10 | results.csv |
| 7     | HashMap.insert   | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:15 | results.csv |
| 8     | HashMap.iterate  | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:20 | results.csv |
| 9     | HashMap.search   | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:25 | results.csv |
| 10    | HashMap.update   | 42   | warmup=5, measure=10, fork=3 | SUCCESS | 2026-05-18 13:30 | results.csv |

Jumlah runs per skenario : 30 (3 forks x 10 iterations)
Total runs               : 1,200 measurements (40 combinations x 30)

DATA LOG (per run):
  Run ID    : RUN-JMH-01
  Timestamp : 2026-05-18T12:44:00
  Skenario  : ArrayList vs HashMap CRUD Performance Benchmark
  Input     : Dataset POJO Person (synthetic, seed 42)
  Output    : benchmark-project/results/results.csv
  Anomali   : Tidak ada error fatal, GC pause terdeteksi minimal
  Catatan   : RAM dialokasikan 4GB fixed heap. Semua CPU background process dimatikan.
```

---

## Latihan 1 — Execution Plan

Susun execution plan untuk eksperimen Anda. Tentukan skenario, jumlah run, dan seed sebelum eksekusi.

| Run # | Skenario | Seed | Parameter Kunci | Status |
|-------|----------|------|----------------|--------|
| 1 | ArrayList.search @ 10³ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 2 | ArrayList.search @ 10⁴ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 3 | ArrayList.search @ 10⁵ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 4 | ArrayList.search @ 10⁶ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 5 | HashMap.search @ 10³ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 6 | HashMap.search @ 10⁴ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 7 | HashMap.search @ 10⁵ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| 8 | HashMap.search @ 10⁶ | 42 | warmup=5, measure=10, fork=3 |  Completed |
| ... | (40 kombinasi total) | 42 | Same config |  All Completed |

**Total skenario:** 40 (2 struktur × 5 operasi × 4 ukuran × 2 modes)
**Run per skenario:** 30 samples (3 forks × 10 iterations)
**Total run keseluruhan:** 1,200 measurements (40 × 30)
**Durasi eksekusi:** ~60 menit (2026-05-18, 12:44 - 13:12)

---

## Latihan 2 — Data Log Terstruktur

Desain format data log untuk eksperimen Anda. Tentukan field apa saja yang akan dicatat.

**Identitas:**
| Field | Contoh |
|-------|--------|
| Benchmark | com.research.benchmark.ArrayListBenchmark.search |
| Mode | avgt (AverageTime) / thrpt (Throughput) |
| Timestamp | 2026-05-18T13:12:30 |
| Param: datasetSize | 1000 / 10000 / 100000 / 1000000 |

**Konfigurasi:**
| Field | Value |
|-------|-------|
| Seed | 42 (DatasetGenerator) |
| JVM Version | OpenJDK 17 LTS |
| JVM Flags | -Xms4g -Xmx4g -XX:+UseG1GC -XX:+AlwaysPreTouch |
| Warmup | 5 iterations × 1 second |
| Measurement | 10 iterations × 1 second |
| Forks | 3 (isolated JVM instances) |

**Hasil:**
| Metrik | Tipe Data | Range Valid |
|--------|----------|-------------|
| Score (mean) | double | > 0 (ns/op atau ops/ns) |
| Score Error (99.9%) | double | > 0 (margin of error) |
| Samples | int | 30 (3 forks × 10 iterations) |
| Threads | int | 1 (single-threaded) |
| Unit | string | "ns/op" atau "ops/ns" |

**Format output:** [X] CSV / [ ] JSON / [ ] Database
**File:** `results/results.csv` (80 rows, 9 columns)

---

## Latihan 3 — Anomaly Protocol

Rencanakan bagaimana menangani anomali. Untuk setiap jenis, tentukan langkah yang diambil.

| Jenis Anomali | Contoh | Tindakan |
|---------------|--------|----------|
| Run gagal (crash) | Compilation error di HashMapBenchmark.update |  Fixed source code, rebuild JAR, re-run full benchmark |
| Hasil ekstrem | Score Error > Score (CI sangat lebar) |  Documented di log, acceptable karena JMH capture variability |
| Waktu eksekusi anomali | GC pause di tengah measurement |  JMH GC profiler aktif, lapor dengan/tanpa GC pause |
| Inkonsistensi dengan run lain | Duplikasi BenchmarkList (20 entries, harusnya 10) |  Investigated, caused by 2 modes (avgt + thrpt), not a bug |
| JAR corrupt | First run failed with compilation error |  Rebuild dengan `mvn clean package`, verify with `-l` flag |

**Prinsip:** Detect → Investigate → Document → Decide

---

## Refleksi

> Pernahkah Anda melaporkan hasil riset/tugas dari single run? Apa risikonya? Bagaimana multiple run mengubah kepercayaan terhadap hasil?

**Pengalaman sebelumnya:**
> Sebelum menggunakan JMH, saya pernah mengukur performa dengan `System.currentTimeMillis()` single-run. Hasilnya tidak konsisten antar-run (bisa beda 2-3x) karena:
> - Tidak ada warmup → JIT belum optimize
> - Single measurement → tidak capture variability
> - Resolusi timer rendah (~15ms di Windows)
> - GC bisa terjadi di tengah measurement

**Yang akan dilakukan berbeda:**
> Dengan JMH + multiple runs:
> -  5 warmup iterations untuk stabilkan JIT
> -  10 measurement iterations untuk capture distribusi
> -  3 forks untuk isolasi antar-run
> -  Confidence interval 99.9% untuk quantify uncertainty
> -  GC profiler untuk detect anomali
> -  Hasil reproducible dengan seed=42
> 
> **Kesimpulan:** Multiple runs dengan JMH menghasilkan data yang **reliable, reproducible, dan statistically valid** untuk decision making.
