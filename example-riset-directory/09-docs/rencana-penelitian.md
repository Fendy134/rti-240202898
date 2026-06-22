# Rencana Penelitian

**Judul:** Analisis Perbandingan Performa Penggunaan ArrayList vs HashMap dalam Manajemen Data Objek pada Bahasa Pemrograman Java

**Peneliti:** [Nama Peneliti]  
**Target Publikasi:** Sinta 3-4 atau Konferensi Nasional  

---

## Ringkasan Topik

Penelitian ini mengevaluasi secara empiris perbedaan performa antara **ArrayList** dan **HashMap** pada Java 17 LTS untuk 5 operasi CRUD dasar (insert, search, update, delete, iterate) dengan 4 ukuran dataset (10³–10⁶ elemen), menggunakan **JMH (Java Microbenchmark Harness)** untuk timing presisi dan **JOL (Java Object Layout)** untuk memory footprint measurement.

**Problem:** Developer Java sering memilih struktur data berdasarkan intuisi tanpa panduan empiris yang valid.

**Gap:** Belum ada studi yang membandingkan ArrayList vs HashMap dengan metodologi benchmark rigorous (JMH + statistical testing) pada Java 17 LTS.

**Contribution:** Baseline empiris performa + decision matrix praktis untuk developer + memory footprint measurement akurat.

---

## Roadmap Penelitian

### Fase 1: Persiapan (Minggu 1-4)

| Minggu | Aktivitas | Output | Referensi |
|---|---|---|---|
| 1-2 | **WS-01 sampai WS-04**: Problem definition, literature review, gap analysis, RQ & hypothesis | Proposal awal (latar belakang, gap, RQ, hipotesis) | [../01-proposal/](../01-proposal/) |
| 3-4 | **WS-05 sampai WS-07**: Variable definition, metrics design, system architecture (JMH+JOL), experiment design | Proposal lengkap (variabel, metrik, sistem, desain eksperimen, threat analysis) | [../01-proposal/proposal-penelitian.md](../01-proposal/proposal-penelitian.md) |
| 5 (UTS) | **WS-08**: Proposal integration — kompilasi proposal, integration checklist, self-assessment | Proposal final dengan integration map (Problem → Gap → RQ → Metrik → Sistem → Eksperimen) | [../01-proposal/](../01-proposal/), [../00-admin/jadwal-dan-log-penelitian.md](../00-admin/jadwal-dan-log-penelitian.md) |

**Deliverable:** Proposal penelitian lengkap dengan verifikasi 6 koneksi integration map.

---

### Fase 2: Implementasi (Minggu 6-7)

| Minggu | Aktivitas | Output | Referensi |
|---|---|---|---|
| 6 | Setup environment (Java 17 LTS, Maven), implementasi model data Person, dataset generator (seed=42) | `Person.java`, `DatasetGenerator.java` | [../05-kode/](../05-kode/) |
| 7 | Implementasi benchmark harness JMH (5 operasi × 2 struktur data), memory profiler JOL | `ArrayListBenchmark.java`, `HashMapBenchmark.java`, `MemoryProfiler.java` | [../05-kode/README_KODE.md](../05-kode/README_KODE.md) |

**Deliverable:** Benchmark harness JMH + JOL yang verified (build success, test run sukses).

**Verifikasi:**
```bash
cd ../../benchmark-project/
mvn clean package
# Test run kecil
java -jar target/benchmarks.jar "ArrayListBenchmark.search" -p datasetSize=1000 -wi 1 -i 2 -f 1
```

---

### Fase 3: Eksekusi (Minggu 8)

| Minggu | Aktivitas | Output | Referensi |
|---|---|---|---|
| 8 | **WS-12**: Eksekusi benchmark penuh (40 kombinasi × 3 forks × 10 iterations = 1200 data points) + memory profiling | `results.csv` (1200 data points), `memory_footprint.csv` | [../04-data/](../04-data/), [tahap-2-eksekusi-benchmark.md](tahap-2-eksekusi-benchmark.md) |

**Estimasi waktu:** 2-4 jam (tergantung hardware).

**Command:**
```bash
# Memory profiler
java -cp target/benchmarks.jar com.research.benchmark.MemoryProfiler \
    > results/memory_footprint.csv

# JMH benchmark
java -jar target/benchmarks.jar -rf csv -rff results/results.csv
```

**Deliverable:** Data mentah benchmark (1200 measurements) + memory footprint (8 data points).

---

### Fase 4: Analisis (Minggu 9-10)

| Minggu | Aktivitas | Output | Referensi |
|---|---|---|---|
| 9 | **WS-13**: Data validation (outlier detection Z-score), descriptive statistics (mean, median, std, CI99, CV) | `descriptive_stats.csv` | [../06-output/](../06-output/), [tahap-3-analisis-visualisasi.md](tahap-3-analisis-visualisasi.md) |
| 10 | **WS-14**: Statistical analysis (Two-way ANOVA, Tukey HSD, Bonferroni correction, Cohen's d), visualisasi (5 figure PNG) | `anova_results.csv`, `pairwise_comparison.csv`, `effect_sizes.csv`, `decision_matrix.csv`, 5 figure PNG | [../06-output/HASIL_ANALISIS.md](../06-output/HASIL_ANALISIS.md) |

**Statistical plan:**
- Two-way ANOVA (struktur data × ukuran dataset)
- Pairwise comparison: Tukey HSD
- Multiple testing correction: Bonferroni (α = 0.0025)
- Effect size: Cohen's d (threshold 0.5)

**Deliverable:** 6 tabel CSV + 5 figure PNG + interpretasi hasil.

---

### Fase 5: Penulisan (Minggu 11-14)

| Minggu | Aktivitas | Output | Referensi |
|---|---|---|---|
| 11-12 | **WS-15**: Penulisan laporan penelitian (metodologi, hasil, diskusi, kesimpulan, limitation & future work) | Laporan penelitian lengkap | [../08-laporan/laporan-penelitian.md](../08-laporan/laporan-penelitian.md) |
| 12 | Penulisan draft paper/manuskrip (Abstrak, Pendahuluan, Tinjauan Pustaka, Metodologi, Hasil, Diskusi, Kesimpulan) | Draft paper | [../07-manuskrip/](../07-manuskrip/) |
| 13-14 (UAS) | **WS-16**: Persiapan presentasi & defense (slide deck 9 slides, anticipatory defense matrix, simulasi Q&A) | Slide deck + defense matrix | [../../ws-16-presentation-defense.md](../../ws-16-presentation-defense.md) |

**Deliverable:** Laporan penelitian lengkap + draft paper + slide presentasi.

---

## Timeline Ringkas

```
Minggu 1-4   : Persiapan (Problem, Gap, RQ, Proposal)
Minggu 5     : UTS — Proposal Integration
Minggu 6-7   : Implementasi (Setup, JMH harness, JOL profiler)
Minggu 8     : Eksekusi (Benchmark penuh 1200 data points)
Minggu 9-10  : Analisis (Statistical testing, Visualisasi)
Minggu 11-12 : Penulisan (Laporan, Draft paper)
Minggu 13-14 : UAS — Presentasi & Defense
```

**Total durasi:** 14 minggu (~3.5 bulan)

---

## Kriteria Keberhasilan

| Kriteria | Target | Verifikasi |
|---|---|---|
| **Proposal lengkap** | 6 koneksi integration map verified | ✓ Checklist WS-08 |
| **Benchmark harness** | Build success, test run sukses | ✓ `mvn clean package` |
| **Data mentah** | 1200 measurements, no missing data | ✓ `results.csv` 40 kombinasi × 30 data points |
| **Validasi data** | No outlier ekstrem (Z-score < 3), CV < 50% | ✓ `01_validate_data.py` |
| **Statistical analysis** | ANOVA p < 0.05, effect size Cohen's d > 0.5 | ✓ `anova_results.csv`, `effect_sizes.csv` |
| **Visualisasi** | 5 figure PNG (execution time, memory, speedup, decision matrix) | ✓ `06-output/figures/` |
| **Decision matrix** | Rekomendasi struktur data per operasi × ukuran | ✓ `decision_matrix.csv` |
| **Laporan** | Lengkap (metodologi, hasil, diskusi, kesimpulan) | ✓ `08-laporan/laporan-penelitian.md` |
| **Presentasi** | Slide deck 9 slides, anticipatory defense matrix | ✓ WS-16 template |

---

## Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| **Benchmark terlalu lama** (>4 jam) | Timeline molor | Reduce iterations (`-wi 2 -i 5 -f 1`) untuk testing, full run saat idle |
| **Measurement variance tinggi** (CV > 50%) | Data tidak reliable | Increase iterations, close background apps, check thermal throttling |
| **Outlier ekstrem** | Bias hasil statistik | Outlier detection (Z-score), report outlier di limitation |
| **ANOVA tidak signifikan** | H₀ tidak ditolak | Report as-is (negative result valid), analisis mengapa tidak signifikan |
| **Hardware terbatas** (RAM <8GB) | JVM crash | Reduce heap (`-Xms2g -Xmx2g`), reduce dataset max size (10⁵ bukan 10⁶) |

---

## Checklist Tahapan

- [x] **WS-01 sampai WS-04**: Problem, Gap, RQ, Hipotesis
- [x] **WS-05 sampai WS-07**: Variabel, Metrik, Sistem, Desain Eksperimen
- [x] **WS-08**: Proposal Integration (UTS)
- [x] **WS-09 sampai WS-11**: Setup & Implementasi benchmark harness
- [x] **WS-12**: Eksekusi benchmark penuh (1200 data points)
- [x] **WS-13 sampai WS-14**: Analisis statistik & visualisasi
- [x] **WS-15**: Penulisan laporan & draft paper
- [x] **WS-16**: Presentasi & Defense (UAS)

---

## Referensi Dokumen

- Proposal penelitian: [../01-proposal/proposal-penelitian.md](../01-proposal/proposal-penelitian.md)
- Matriks literatur: [../02-literatur/matriks-literatur.md](../02-literatur/matriks-literatur.md)
- Teori kompleksitas: [../03-teori/kompleksitas-dan-karakteristik.md](../03-teori/kompleksitas-dan-karakteristik.md)
- Source code: [../05-kode/README_KODE.md](../05-kode/README_KODE.md)
- Hasil analisis: [../06-output/HASIL_ANALISIS.md](../06-output/HASIL_ANALISIS.md)
- Laporan penelitian: [../08-laporan/laporan-penelitian.md](../08-laporan/laporan-penelitian.md)
- Jadwal & log: [../00-admin/jadwal-dan-log-penelitian.md](../00-admin/jadwal-dan-log-penelitian.md)
