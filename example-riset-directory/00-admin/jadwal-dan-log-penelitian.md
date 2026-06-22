# Jadwal & Log Pelaksanaan Penelitian

Catatan kronologis pelaksanaan tiap tahap penelitian ArrayList vs HashMap. Tanggal mengikuti timeline WS-01 sampai WS-16.

## Log Pelaksanaan

| Tanggal | Tahap | Aktivitas | Referensi |
|---|---|---|---|
| Minggu 1-2 | WS-01 sampai WS-04 | Problem definition, literature review, gap analysis, research question & hypothesis formulation | [../ws-02-problem-definition.md](../../ws-02-problem-definition.md), [../ws-03-literature-gap.md](../../ws-03-literature-gap.md), [../ws-04-research-question.md](../../ws-04-research-question.md) |
| Minggu 3-4 | WS-05 sampai WS-07 | Variable definition, metrics design, system architecture (JMH + JOL), experiment design, threat analysis | [../ws-05-variable-metric.md](../../ws-05-variable-metric.md), [../ws-06-system-design.md](../../ws-06-system-design.md), [../ws-07-experiment-design.md](../../ws-07-experiment-design.md) |
| Minggu 5 (UTS) | WS-08 | Proposal integration — kompilasi proposal lengkap, integration checklist, self-assessment | [../ws-08-proposal-integration.md](../../ws-08-proposal-integration.md), [01-proposal/](../01-proposal/) |
| Minggu 6-7 | WS-09 sampai WS-11 | Setup environment (Java 17 LTS, Maven), implementasi benchmark harness (JMH + JOL), implementasi model Person, dataset generator (seed=42), 5 operasi CRUD ArrayList & HashMap | [09-docs/tahap-1-setup-implementasi.md](../09-docs/tahap-1-setup-implementasi.md), [05-kode/](../05-kode/) |
| Minggu 8 | WS-12 | Eksekusi benchmark penuh — ArrayList & HashMap (5 operasi × 4 ukuran × 3 forks × 10 iterations) + memory profiling JOL | [09-docs/tahap-2-eksekusi-benchmark.md](../09-docs/tahap-2-eksekusi-benchmark.md), [04-data/](../04-data/) |
| Minggu 9-10 | WS-13 sampai WS-14 | Analisis statistik (Two-way ANOVA, Tukey HSD, Bonferroni correction), visualisasi (execution time, memory footprint, speedup ratio, decision matrix), interpretasi hasil | [09-docs/tahap-3-analisis-visualisasi.md](../09-docs/tahap-3-analisis-visualisasi.md), [06-output/](../06-output/) |
| Minggu 11-12 | WS-15 | Penulisan laporan penelitian (metodologi, hasil, diskusi, kesimpulan, limitation & future work) | [08-laporan/laporan-penelitian.md](../08-laporan/laporan-penelitian.md), [07-manuskrip/](../07-manuskrip/) |
| Minggu 13-14 (UAS) | WS-16 | Persiapan presentasi & defense — slide deck, anticipatory defense matrix, simulasi Q&A | [../ws-16-presentation-defense.md](../../ws-16-presentation-defense.md) |

## Status Ringkas

- **Tahap 1 (Setup & Implementasi)**: Selesai — JMH harness, JOL profiler, 5 operasi × 2 struktur data
- **Tahap 2 (Eksekusi Benchmark)**: Selesai — dataset final n=30 per kombinasi (total 1200 data points)
- **Tahap 3 (Analisis & Visualisasi)**: Selesai — ANOVA, pairwise comparison, 5 figure PNG, decision matrix
- **Tahap 4 (Laporan & Manuskrip)**: Selesai — laporan penelitian lengkap
- **Tahap 5 (Presentasi & Defense)**: Selesai — slide deck 9 slides, anticipatory defense matrix

## Item Tindak Lanjut (Checklist Sebelum Submission)

- [x] Verifikasi semua koneksi integration map (Problem → Gap → RQ → Metrik → Sistem → Eksperimen)
- [x] Jalankan benchmark penuh (5 operasi × 4 ukuran × 2 struktur data × 3 forks × 10 iterations)
- [x] Validasi data mentah (outlier detection via Z-score |z| > 3, data cleaning)
- [x] Analisis statistik inferensial (ANOVA p < 0.05, Bonferroni correction α = 0.0025)
- [x] Visualisasi hasil (execution time heatmap, memory footprint bar chart, speedup ratio line plot, decision matrix heatmap)
- [x] Interpretasi boundary conditions (ArrayList.iterate TIE pada 1M elemen, HashMap.insert overhead pada dataset kecil)
- [x] Dokumentasi threat to validity & mitigasi (JIT warmup, GC overhead, hardware variability)
- [x] Decision matrix untuk developer (operasi dominan × ukuran dataset → rekomendasi struktur data)
- [x] Laporan penelitian lengkap dengan seluruh komponen (metodologi, hasil, diskusi, kesimpulan)
- [x] Slide deck presentasi (9 slides, 15 menit) + anticipatory defense matrix

## Korespondensi

- **2026-03-15**: Konsultasi pembimbing — approval research question & hypothesis
- **2026-04-10**: Konsultasi pembimbing — review experiment design & threat analysis
- **2026-05-12**: Konsultasi pembimbing — review hasil statistik & interpretasi
- **2026-06-01**: Konsultasi pembimbing — review draft laporan & decision matrix
