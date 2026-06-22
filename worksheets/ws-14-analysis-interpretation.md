# WS-14: Analysis, Interpretation & Failure Analysis

> **Bab 14 — Analisis Data, Interpretasi & Failure Analysis**

---

## Ringkasan Materi

### Data → Knowledge Model

```
Data → Analysis → Interpretation → Explanation → Knowledge
```

Tiga level yang berbeda:
- **Analysis** — "Apa yang terjadi?" (deskriptif + inferensial)
- **Interpretation** — "Apa artinya?" (konteks RQ + literatur)
- **Failure Analysis** — "Mengapa tidak berhasil?" (boundary conditions)

### Beyond p-value

**Statistical significance ≠ practical significance.** Selalu laporkan:
1. p-value (signifikansi statistik)
2. Effect size (besarnya efek)
3. Confidence interval (rentang ketidakpastian)

| Effect Size (Cohen's d) | Interpretasi |
|-------------------------|-------------|
| < 0.2 | Small |
| 0.2 – 0.8 | Medium |
| > 0.8 | Large |

### Pemilihan Uji Statistik

| Kondisi | Uji yang Tepat |
|---------|---------------|
| 2 grup, normal, paired | Paired t-test |
| 2 grup, non-normal | Wilcoxon signed-rank |
| > 2 grup, normal | One-way ANOVA + post-hoc |
| > 2 grup, non-normal | Kruskal-Wallis + post-hoc |
| 2 variabel kontinu | Pearson (normal) / Spearman (rank) |

### Failure Analysis as Contribution

Hipotesis yang ditolak adalah **temuan yang berharga**:

| Dataset | New (F1) | Baseline (F1) | p-value | Cohen's d |
|---------|---------|--------------|---------|-----------|
| DS-1 (small, clean) | 94.2±1.1 | 89.3±1.5 | <0.001 | **3.7** |
| DS-4 (medium, noisy) | 78.3±3.2 | 82.1±2.8 | 0.008 | **-1.3** |
| DS-5 (large, noisy) | 71.6±4.1 | 80.5±3.0 | <0.001 | **-2.5** |

**Insight:** Metode baru unggul di data bersih tapi gagal di data noisy → asumsi Gaussian dilanggar → **boundary condition** ditemukan → hybrid approach direkomendasikan.

**Partial failure + deep analysis = kontribusi lebih kaya daripada full success tanpa analisis.**

### Limitation Types

| Jenis | Contoh |
|-------|--------|
| Internal validity | Confounders yang tidak dikontrol |
| External validity | Generalisasi ke domain lain |
| Construct validity | Metrik mengukur apa yang dimaksud? |
| Statistical limitation | Sample size, asumsi distribusi |

### Jebakan Kognitif

1. "Signifikan statistik = penting secara praktis" → cek effect size
2. "Hipotesis tidak didukung → cari sudut baru" → p-hacking
3. "Kegagalan tidak perlu dilaporkan detail" → missed insight
4. "Limitasi cukup disebutkan, tidak perlu dianalisis" → kedalaman hilang

---

## Template A.14 — Analysis & Interpretation Report

```
ANALYSIS & INTERPRETATION

1. Statistik Deskriptif:
   | Skenario | Mean | Std | Median | Min | Max | n |
   |----------|------|-----|--------|-----|-----|---|
   | ArrayList.search @ 1M | 7,459,142.3 | 2,204,828.8 | 7,450,000.0 | 4,200,000.0 | 12,000,000.0 | 30 |
   | HashMap.search @ 1M   | 70.8        | 39.6        | 70.0        | 20.0        | 150.0        | 30 |

2. Uji Hipotesis:
   Uji yang digunakan  : Two-way ANOVA & Tukey HSD Post-hoc Test (log-transformed)
   Justifikasi          : Membandingkan 2 tipe struktur data pada beberapa ukuran dataset dan operasi. Data ditransformasikan ke log karena variansi tidak homogen.
   Hasil: p < 0.0001, effect size (Cohen's d) = 4.7844 (Large Effect)
   CI 99.9% (JMH)       : ArrayList [6,349,573.4, 8,568,711.2] ns vs HashMap [50.8, 90.7] ns

3. Keputusan:
   [x] H₀ ditolak → H₁ diterima
   [ ] H₀ tidak ditolak

4. Interpretasi:
   Hubungan ke RQ       : Membuktikan secara empiris perbedaan performa ArrayList vs HashMap pada operasi CRUD.
   Practical significance: HashMap 94,000x lebih cepat untuk search @ 1M, menghemat waktu eksekusi secara signifikan pada produksi.
   Perbandingan literatur: Konsisten dengan teori kompleksitas O(1) vs O(N), namun menunjukkan overhead resizing pada ArrayList.

5. Limitation:
   | Jenis | Ancaman | Dampak | Mitigasi |
   |-------|---------|--------|----------|
   | External | Data sintetis seragam | Kurang menggambarkan distribusi riil | Uji dengan data non-uniform |
   | Construct| Single-threaded benchmark | Mengabaikan overhead multithreading | Rencana uji dengan concurrent classes |

6. Failure Analysis (jika H₀ tidak ditolak):
   Penyebab potensial  : N/A (H0 berhasil ditolak pada operasi search, delete, update)
   Boundary condition   : Pada iterate @ 1M terjadi TIE karena cache miss ArrayList setara dengan hashing overhead HashMap.
   Insight              : Keunggulan iterasi ArrayList tidak lagi absolut pada dataset berukuran sangat besar.
```

---

## Latihan 1 — Pemilihan Uji Statistik

Tentukan uji statistik yang tepat untuk eksperimen Anda.

| Pertanyaan | Jawaban |
|-----------|---------|
| Berapa grup yang dibandingkan? | 2 grup (ArrayList vs HashMap) per kombinasi operasi × ukuran |
| Apakah data berpasangan (paired)? | Tidak — independent groups (struktur data berbeda) |
| Apakah distribusi normal? (uji normalitas) | Tidak perlu uji formal — JMH sudah provide CI 99.9% dari 30 samples |
| **Uji yang dipilih:** | **Pairwise comparison dengan CI overlap test** + **Speedup ratio** |
| **Justifikasi:** | Data aggregated (mean ± error dari JMH). Bandingkan CI 99.9%: jika tidak overlap → signifikan. |

**Effect size yang akan dilaporkan:** [X] Speedup ratio (praktis untuk benchmark) / [ ] Cohen's d (tidak applicable untuk data aggregated)

---

## Latihan 2 — Interpretasi Hasil

Gunakan data berikut (atau data riil Anda) untuk berlatih interpretasi.

**Data:**
| Model | Accuracy (mean ± std) | n |
|-------|----------------------|---|
| A | 89.2 ± 1.5 | 10 |
| B | 87.8 ± 2.1 | 10 |

p = 0.045, Cohen's d = 0.74, CI 95% = [0.03, 2.77]

| Aspek | Interpretasi |
|-------|-------------|
| Signifikansi statistik | HashMap.search @ 10⁶: CI tidak overlap dengan ArrayList → **signifikan** (p < 0.001 equivalent) |
| Effect size | Speedup ratio = 94,014.7x → **extremely large effect** (HashMap 94,000x lebih cepat) |
| Practical significance | **Sangat signifikan praktis** — perbedaan 7 juta ns vs 75 ns adalah game-changer untuk aplikasi production |
| Hubungan ke RQ | ✅ **Menjawab RQ:** "Bagaimana perbedaan performa ArrayList vs HashMap?" → HashMap dominan di search/delete/update, ArrayList unggul di iterate |
| Perbandingan literatur | ✅ **Konsisten dengan teori:** HashMap O(1) vs ArrayList O(n) terbukti empiris. Gorelick & Ozsvald (2020) menyebutkan HashMap O(1) tapi tidak ada measurement empiris di Java 17 LTS. |

---

## Latihan 3 — Failure Analysis

Latih kemampuan failure analysis: hipotesis TIDAK didukung. Apa yang bisa dipelajari?

**Skenario:** Metode baru Anda mendapat F1 = 83.2%, baseline = 84.7%. p = 0.12 (tidak signifikan).

| Pertanyaan | Jawaban |
|-----------|---------|
| Apakah ini "gagal"? | **Tidak ada failure** — semua hipotesis terdukung. H1a (HashMap faster di search) ✅, H1b (ArrayList faster di iterate) ✅ |
| Kemungkinan penyebab? | N/A — hasil sesuai ekspektasi teori (HashMap O(1), ArrayList O(n)) |
| Boundary condition? | **Ditemukan:** ArrayList.iterate @ 10⁶ = TIE. Pada dataset sangat besar, cache miss di ArrayList mulai comparable dengan HashMap overhead. |
| Insight yang bisa diambil? | **Trade-off:** HashMap insert @ 10K = 16x slower karena rehashing. **Rekomendasi:** ArrayList untuk append, HashMap untuk lookup-heavy. |
| Apakah layak dilaporkan? Mengapa? | ✅ **Ya** — boundary condition (iterate @ 10⁶ = TIE) adalah temuan penting. Menunjukkan "ArrayList always faster di iterate" tidak absolut. |

**Limitation terkait:**
| Jenis | Ancaman | Dampak |
|-------|---------|--------|
| **External validity** | Dataset synthetic (uniform random) | Hasil mungkin berbeda di real-world data (skewed, clustered) |
| **External validity** | Single-threaded saja | Tidak bisa generalisasi ke concurrent scenario |
| **Construct validity** | Memory footprint tidak diukur langsung | Hanya execution time, tidak ada data memory usage |
| **Statistical** | High variability (Error > Score) | CI sangat lebar untuk operasi sangat cepat |

---

## Refleksi

> Apakah "failure" dalam riset benar-benar gagal, atau justru kontribusi? Bagaimana failure analysis mengubah cara Anda melihat hasil negatif?

> Dalam riset ilmiah, "failure" atau kegagalan dalam menolak hipotesis nol (H0 tidak ditolak) bukanlah kegagalan penelitian, melainkan penemuan ilmiah yang berharga. Kegagalan tersebut menyingkap *boundary conditions* (kondisi batas) dari suatu metode atau teori yang sebelumnya tidak disadari. Melalui *failure analysis* yang mendalam, peneliti dapat memahami faktor penyebab (seperti *rehashing overhead*, *cache locality*, atau *garbage collection*), memetakan kelemahan sistematis, dan memberikan kontribusi berupa batasan teoretis serta praktis. Hasil negatif yang dianalisis secara objektif dan mendalam justru mencegah peneliti lain melakukan kesalahan yang sama dan memberikan fondasi yang kuat untuk arah riset masa depan.
