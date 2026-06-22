# 09-docs — Dokumentasi Perencanaan & Tahapan Penelitian

Folder ini berisi dokumen perencanaan dan panduan pelaksanaan penelitian ArrayList vs HashMap.

## Isi Folder

| File | Deskripsi | Status |
|---|---|---|
| [rencana-penelitian.md](rencana-penelitian.md) | **Indeks utama** — ringkasan topik, roadmap 5 fase (14 minggu), timeline, kriteria keberhasilan | ✅ Selesai |
| [tahap-1-setup-implementasi.md](tahap-1-setup-implementasi.md) | Tahap 1 — Setup environment, implementasi benchmark harness JMH, memory profiler JOL, model data Person | ✅ Selesai |
| [tahap-2-eksekusi-benchmark.md](tahap-2-eksekusi-benchmark.md) | Tahap 2 — Eksekusi benchmark penuh (40 kombinasi × 30 data points = 1200 measurements) + memory profiling | ✅ Selesai |
| [tahap-3-analisis-visualisasi.md](tahap-3-analisis-visualisasi.md) | Tahap 3 — Analisis statistik (ANOVA, Tukey HSD, Cohen's d) + visualisasi (5 figure PNG) + decision matrix | ✅ Selesai |
| [tahap-4-penulisan-laporan.md](tahap-4-penulisan-laporan.md) | Tahap 4 — Penulisan laporan penelitian lengkap + draft naskah jurnal/paper + verifikasi konsistensi angka | ✅ Selesai |
| [tahap-5-presentasi-defense.md](tahap-5-presentasi-defense.md) | Tahap 5 — Slide deck presentasi (9-10 slides) + anticipatory defense matrix + simulasi Q&A | ✅ Selesai |

## Overview Tahapan

### Fase 1: Persiapan (Minggu 1-5)
- **WS-01 sampai WS-04**: Problem definition, literature review, gap analysis, RQ & hypothesis
- **WS-05 sampai WS-07**: Variable definition, metrics design, system architecture, experiment design
- **WS-08 (UTS)**: Proposal integration & self-assessment

### Fase 2: Implementasi (Minggu 6-7)
- **Tahap 1**: Setup environment (Java 17 LTS, Maven), implementasi benchmark harness JMH + JOL
- Deliverable: `Person.java`, `DatasetGenerator.java`, `ArrayListBenchmark.java`, `HashMapBenchmark.java`, `MemoryProfiler.java`

### Fase 3: Eksekusi (Minggu 8)
- **Tahap 2**: Eksekusi benchmark penuh (1200 measurements) + memory profiling (8 data points)
- Estimasi waktu: 2-4 jam
- Deliverable: `results.csv`, `memory_footprint.csv`

### Fase 4: Analisis (Minggu 9-10)
- **Tahap 3**: Data validation, descriptive statistics, inferential statistics (ANOVA, Tukey HSD), effect size (Cohen's d), visualisasi
- Deliverable: 6 tabel CSV + 5 figure PNG + decision matrix

### Fase 5: Penulisan & Presentasi (Minggu 11-14)
- **Tahap 4 (WS-15)**: Penulisan laporan penelitian + draft naskah jurnal
- **Tahap 5 (WS-16/UAS)**: Slide deck presentasi + anticipatory defense matrix + simulasi Q&A

## Deliverable Per Tahap

| Tahap | Folder Output | Deliverable Utama |
|---|---|---|
| **Tahap 1** | [05-kode/](../05-kode/) | Source code benchmark JMH + JOL |
| **Tahap 2** | [04-data/](../04-data/) | Data mentah (1200 measurements) |
| **Tahap 3** | [06-output/](../06-output/) | Tabel statistik + visualisasi + decision matrix |
| **Tahap 4** | [08-laporan/](../08-laporan/) + [07-manuskrip/](../07-manuskrip/) | Laporan penelitian lengkap + draft naskah jurnal |
| **Tahap 5** | [Slide deck](../07-manuskrip/) + Defense matrix | Presentasi & defense (UAS) |

## Referensi Cepat

- **Proposal penelitian**: [../01-proposal/proposal-penelitian.md](../01-proposal/proposal-penelitian.md)
- **Matriks literatur**: [../02-literatur/matriks-literatur.md](../02-literatur/matriks-literatur.md)
- **Teori kompleksitas**: [../03-teori/kompleksitas-dan-karakteristik.md](../03-teori/kompleksitas-dan-karakteristik.md)
- **Source code**: [../05-kode/README_KODE.md](../05-kode/README_KODE.md)
- **Hasil analisis**: [../06-output/HASIL_ANALISIS.md](../06-output/HASIL_ANALISIS.md)
- **Laporan penelitian**: [../08-laporan/laporan-penelitian.md](../08-laporan/laporan-penelitian.md)

## Cara Menggunakan Dokumen Ini

1. **Mulai dari** [rencana-penelitian.md](rencana-penelitian.md) untuk overview lengkap roadmap
2. **Ikuti tahapan** sesuai urutan (Tahap 1 → 2 → 3)
3. **Setiap tahap** berisi:
   - Tujuan dan deliverable
   - Aktivitas dan implementasi
   - Verifikasi hasil
   - Kendala & solusi
   - Status completion

## Checklist Progress

- [x] **Tahap 1** — Setup & Implementasi
- [x] **Tahap 2** — Eksekusi Benchmark
- [x] **Tahap 3** — Analisis & Visualisasi
- [x] **Tahap 4** — Penulisan Laporan & Manuskrip
- [x] **Tahap 5** — Presentasi & Defense
