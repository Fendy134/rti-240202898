# Matriks Literatur

Ringkasan paper dan referensi terkait perbandingan performa struktur data Java.

## Tabel Matriks Literatur

| # | Penulis | Tahun | Judul | Fokus | Metodologi | Gap | Referensi |
|---|---------|-------|-------|-------|------------|-----|-----------|
| 1 | Pujiono & Sitanggang | 2024 | Analisis Perbandingan Performa Algoritma Pengurutan pada Bahasa Pemrograman Java | Sorting algorithms (Bubble, Insertion, Selection, Merge, Quick) | `System.currentTimeMillis()`, single-run, dataset 10K–100K | Tidak ada warmup JVM, tidak ada uji statistik, fokus sorting bukan struktur data | JTIM: Jurnal Teknologi Informasi dan Multimedia, 6(2), 149-156 |
| 2 | Gorelick & Ozsvald | 2020 | High Performance Python: Practical Performant Programming for Humans | Python performance optimization (list, dict, set) | Profiling tools (cProfile, memory_profiler), timeit | Fokus Python bukan Java, tidak ada JMH, tidak ada statistical testing | O'Reilly Media |
| 3 | Evans | 2018 | Optimizing Java: Practical Techniques for Improving JVM Application Performance | JVM optimization, JIT compiler, GC tuning | JMH untuk microbenchmarking, profiling tools (JFR, JMC) | Bukan comparison ArrayList vs HashMap, fokus tuning JVM | O'Reilly Media |
| 4 | Oracle | 2023 | Java Platform, Standard Edition 17 API Specification | Java Collections Framework documentation | N/A (dokumentasi API) | Hanya dokumentasi teoretis, tidak ada benchmark empiris | https://docs.oracle.com/en/java/javase/17/ |
| 5 | JMH Team | 2024 | JMH (Java Microbenchmark Harness) | Framework untuk microbenchmarking Java | Sample benchmarks (String concatenation, HashMap get) | Tidak ada comparison ArrayList vs HashMap yang komprehensif | https://github.com/openjdk/jmh |

## Gap Literatur yang Diidentifikasi

Berdasarkan tinjauan literatur di atas, **gap penelitian** yang teridentifikasi:

1. **Belum ada studi yang membandingkan ArrayList vs HashMap menggunakan JMH pada Java 17 LTS** dengan statistical significance testing dan multi-size dataset (10³–10⁶).

2. **Studi existing (Pujiono et al. 2024) menggunakan metodologi benchmark yang lemah**:
   - `System.currentTimeMillis()` dengan single-run tanpa warmup
   - Tidak ada kontrol terhadap JIT compiler dan GC
   - Tidak ada uji signifikansi statistik (ANOVA, t-test)
   
3. **Tidak ada measurement akurat untuk memory footprint** — existing studies fokus pada execution time saja, tidak mengukur memory overhead menggunakan tools seperti JOL.

4. **Tidak ada decision matrix praktis** untuk developer — sebagian besar paper fokus pada analisis teoretis (Big-O notation) tanpa panduan empiris untuk pemilihan struktur data.

5. **Dataset terbatas pada ukuran kecil** (<10K elemen) — tidak ada evaluasi pada dataset besar (100K–1M) yang mencerminkan aplikasi production.

## Kontribusi Penelitian Ini

Penelitian ini mengisi gap dengan:

1. **Perbandingan empiris ArrayList vs HashMap** pada 5 operasi CRUD dasar dengan 4 ukuran dataset (10³–10⁶) menggunakan **JMH v1.37** pada **Java 17 LTS**.

2. **Statistical significance testing** — ANOVA + Tukey HSD + Bonferroni correction untuk memastikan perbedaan signifikan, bukan noise measurement.

3. **Memory footprint measurement** menggunakan **JOL v0.17** — tidak hanya execution time, tapi juga memory overhead (shallow size + deep size).

4. **Decision matrix** praktis — rekomendasi struktur data berdasarkan operasi dominan × ukuran dataset.

5. **Reproducible benchmark** — semua kode, konfigurasi, dan dataset tersedia untuk validasi dan ekstensi.

## Referensi Lengkap

1. Pujiono, Ridho Ananda, and Imas Sukaesih Sitanggang. "Analisis Perbandingan Performa Algoritma Pengurutan pada Bahasa Pemrograman Java." *JTIM: Jurnal Teknologi Informasi dan Multimedia* 6.2 (2024): 149-156.

2. Gorelick, Micha, and Ian Ozsvald. *High Performance Python: Practical Performant Programming for Humans*. O'Reilly Media, 2020.

3. Evans, Benjamin J. *Optimizing Java: Practical Techniques for Improving JVM Application Performance*. O'Reilly Media, 2018.

4. Oracle. *Java Platform, Standard Edition 17 API Specification*. 2023. https://docs.oracle.com/en/java/javase/17/

5. JMH Team. *JMH (Java Microbenchmark Harness)*. 2024. https://github.com/openjdk/jmh

6. JOL Team. *JOL (Java Object Layout)*. 2024. https://github.com/openjdk/jol

7. Naftalin, Maurice, and Philip Wadler. *Java Generics and Collections*. O'Reilly Media, 2006.

8. Bloch, Joshua. *Effective Java*. 3rd ed. Addison-Wesley, 2018.
