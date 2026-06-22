# 07-manuskrip

Folder ini berisi draft naskah jurnal/paper untuk publikasi.

## Isi yang Diharapkan

Draf naskah jurnal dengan struktur standar:

1. **Abstrak** — Ringkasan penelitian (latar belakang, metode, hasil, kesimpulan) dalam 150-250 kata
2. **Pendahuluan** — Latar belakang, motivasi, rumusan masalah, kontribusi penelitian
3. **Tinjauan Pustaka (Related Work)** — Review literatur existing, identifikasi gap penelitian
4. **Metodologi** — Variabel (IV, DV, CV), instrumen (JMH, JOL), desain eksperimen, statistical plan
5. **Hasil & Analisis** — Descriptive statistics, ANOVA, pairwise comparison, visualisasi, interpretasi
6. **Diskusi** — Interpretasi hasil, validasi hipotesis, boundary conditions, implikasi praktis
7. **Kesimpulan** — Ringkasan kontribusi, keterbatasan, future work
8. **Daftar Pustaka** — Referensi dalam format IEEE/APA/ACM

## Status

Draft naskah dapat disusun dengan mengacu pada:
- Proposal penelitian: [../01-proposal/proposal-penelitian.md](../01-proposal/proposal-penelitian.md)
- Laporan penelitian: [../08-laporan/laporan-penelitian.md](../08-laporan/laporan-penelitian.md)
- Hasil analisis: [../06-output/HASIL_ANALISIS.md](../06-output/HASIL_ANALISIS.md)
- Matriks literatur: [../02-literatur/matriks-literatur.md](../02-literatur/matriks-literatur.md)

## Template Naskah

### Abstrak

**Contoh struktur:**

> **Background:** Developer Java sering memilih struktur data berdasarkan intuisi tanpa panduan empiris. **Objective:** Penelitian ini membandingkan performa ArrayList vs HashMap pada Java 17 LTS untuk 5 operasi CRUD dengan 4 ukuran dataset (10³–10⁶). **Methods:** Java Microbenchmark Harness (JMH) v1.37 untuk timing, Java Object Layout (JOL) v0.17 untuk memory measurement, Two-way ANOVA + Tukey HSD untuk statistical testing. **Results:** HashMap unggul signifikan pada search/update/delete (speedup hingga 105,000×, p<0.0001), ArrayList unggul pada insert/iterate pada dataset <100K (speedup 2-400×, p<0.0001), dengan boundary condition teridentifikasi pada dataset 1M (cache miss). **Conclusion:** Decision matrix dihasilkan untuk panduan praktis developer dalam memilih struktur data berdasarkan operasi dominan × ukuran dataset.

### Struktur Lengkap

```markdown
# Empirical Performance Comparison of ArrayList vs HashMap in Java 17 LTS

## Abstract
[150-250 kata]

## 1. Introduction
- Latar belakang & motivasi
- Rumusan masalah
- Research question
- Kontribusi penelitian

## 2. Related Work
- Review literatur existing
- Gap penelitian
- Positioning penelitian ini

## 3. Methodology
- Model data (Person POJO)
- Variabel (IV, DV, CV)
- Instrumen (JMH, JOL)
- Matrix eksperimen (40 kombinasi × 30 data points)
- Statistical plan (ANOVA, Tukey HSD, Bonferroni)

## 4. Results
- Descriptive statistics (Table 1)
- ANOVA results (Table 2)
- Pairwise comparison (Table 3)
- Memory footprint (Table 4)
- Visualisasi (Figure 1-4)

## 5. Discussion
- Interpretasi hasil
- Validasi hipotesis
- Boundary conditions
- Implikasi praktis (decision matrix)

## 6. Conclusion
- Ringkasan kontribusi
- Keterbatasan
- Future work

## References
[Format IEEE/APA/ACM]
```

## Tips Penulisan

### 1. Abstrak
- Fokus pada **kontribusi** bukan hanya deskripsi
- Sertakan **angka kunci**: speedup, p-value, effect size
- Hindari jargon teknis berlebihan

### 2. Pendahuluan
- Hook pembaca dengan **real-world problem** (production bottleneck)
- Jelaskan **gap** dengan jelas (existing studies lemah)
- Highlight **novelty**: JMH + statistical testing + memory measurement + decision matrix

### 3. Metodologi
- Jelas dan **reproducible** — cukup detail untuk orang lain replikasi
- Sertakan konfigurasi JMH (warmup, measurement, forks)
- Justifikasi pilihan metodologi (kenapa JMH bukan `System.currentTimeMillis()`)

### 4. Hasil
- **Data-driven** — tabel dan figure sebagai protagonis
- Narasi menjelaskan highlight dari tabel/figure, bukan mengulang semua angka
- Fokus pada **perbedaan signifikan** (p<0.0025) dan **effect size besar** (Cohen's d > 0.8)

### 5. Diskusi
- **Interpretasi** bukan hanya deskripsi
- Hubungkan hasil dengan teori (O(1) vs O(n), cache locality)
- Diskusikan **boundary conditions** (iterate TIE pada 1M)
- **Honest** tentang limitasi (single-threaded, synthetic data)

### 6. Kesimpulan
- Ringkas **kontribusi** dalam 1-2 paragraf
- Jangan introduce informasi baru
- Future work realistis (multithreading, mixed workload)

## Checklist Sebelum Submit

- [ ] Abstrak ≤ 250 kata
- [ ] Semua figure/table direferensi dalam text
- [ ] Semua referensi dicek validitasnya (DOI/URL accessible)
- [ ] Format konsisten (IEEE/APA/ACM sesuai jurnal target)
- [ ] Proofreading (grammar, typo)
- [ ] Reproducibility check: semua konfigurasi/command tersedia di paper/appendix
- [ ] Ethical statement (jika perlu): no human subjects, no proprietary data

## Target Publikasi

### Sinta 3-4
- **Jurnal Teknologi dan Sistem Komputer (JTSK)** — Sinta 3, Bahasa Indonesia/Inggris
- **ILKOM Jurnal Ilmiah** — Sinta 4, Bahasa Indonesia
- **JTIM: Jurnal Teknologi Informasi dan Multimedia** — Sinta 4, Bahasa Indonesia

### Konferensi Nasional
- **SEMNASIF (Seminar Nasional Informatika)** — Terakreditasi
- **SINTAK (Seminar Nasional Teknologi Informasi dan Aplikasi Komputer)** — Terakreditasi

## Referensi Template

- Laporan penelitian lengkap: [../08-laporan/laporan-penelitian.md](../08-laporan/laporan-penelitian.md)
- Hasil analisis: [../06-output/HASIL_ANALISIS.md](../06-output/HASIL_ANALISIS.md)
- Proposal penelitian: [../01-proposal/proposal-penelitian.md](../01-proposal/proposal-penelitian.md)
