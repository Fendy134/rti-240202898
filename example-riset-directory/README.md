# Penelitian ArrayList vs HashMap — Analisis Performa Empiris Java 17 LTS

**Judul:** Analisis Perbandingan Performa Penggunaan ArrayList vs HashMap dalam Manajemen Data Objek pada Bahasa Pemrograman Java

**Target publikasi:** Sinta 3-4 atau Konferensi Nasional

## Ringkasan

Penelitian ini mengevaluasi secara empiris perbedaan performa antara **ArrayList** dan **HashMap** pada Java 17 LTS untuk 5 operasi CRUD dasar (insert, search, update, delete, iterate) dengan 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶ elemen). Benchmark menggunakan **JMH (Java Microbenchmark Harness) v1.37** untuk timing presisi dan **JOL (Java Object Layout) v0.17** untuk memory footprint measurement, dengan uji signifikansi statistik (ANOVA + Tukey HSD + Bonferroni correction).

Hasil menunjukkan perbedaan signifikan (p < 0.0025) pada mayoritas kombinasi operasi-ukuran: HashMap unggul pada operasi search/update/delete (O(1) vs O(n)), ArrayList unggul pada insert dan iterate (cache locality), dengan trade-off memory footprint yang bergantung pada ukuran dataset.

Detail lengkap topik & roadmap: [09-docs/rencana-penelitian.md](09-docs/rencana-penelitian.md)

## Struktur Direktori

| Folder | Isi |
|---|---|
| [00-admin/](00-admin/) | Administrasi penelitian (jadwal, log eksperimen) |
| [01-proposal/](01-proposal/) | Proposal penelitian |
| [02-literatur/](02-literatur/) | Referensi & paper terkait (Tinjauan Pustaka) |
| [03-teori/](03-teori/) | Teori kompleksitas & karakteristik struktur data |
| [04-data/](04-data/) | Data mentah hasil benchmark JMH & memory profiling JOL |
| [05-kode/](05-kode/) | Source code: benchmark JMH & analysis Python |
| [06-output/](06-output/) | Statistik & visualisasi hasil analisis |
| [07-manuskrip/](07-manuskrip/) | Draf naskah jurnal/paper |
| [08-laporan/](08-laporan/) | Laporan progres/akhir penelitian |
| [09-docs/](09-docs/) | Dokumen perencanaan & roadmap tahap-tahap penelitian |

## Status Tahapan

- [x] **Tahap 1** — Setup Environment & Implementasi Benchmark Harness — *Selesai* ([detail](09-docs/tahap-1-setup-implementasi.md))
- [x] **Tahap 2** — Eksekusi Benchmark Penuh (ArrayList & HashMap) — *Selesai* ([detail](09-docs/tahap-2-eksekusi-benchmark.md))
- [x] **Tahap 3** — Analisis Statistik & Visualisasi — *Selesai* ([detail](09-docs/tahap-3-analisis-visualisasi.md))
- [x] **Tahap 4** — Penulisan Laporan & Manuskrip — *proses*
- [x] **Tahap 5** — presentation defense - **proses*
## Laporan Penelitian

Laporan penelitian komprehensif (ringkasan eksekutif, metodologi per tahap, hasil, kendala, kesimpulan): [08-laporan/laporan-penelitian.md](08-laporan/laporan-penelitian.md)

## Author

[Fendy Agustian]
