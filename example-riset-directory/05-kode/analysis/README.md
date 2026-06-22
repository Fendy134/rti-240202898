# Analysis Scripts — ArrayList vs HashMap Benchmark

Tiga script Python untuk analisis data hasil JMH, sesuai proposal E.5 dan F.

---

## Urutan Eksekusi

```
Minggu 3 selesai → hasil JMH ada di results/
        ↓
01_validate_data.py      ← validasi completeness, consistency, validity
        ↓
02_statistical_analysis.py ← ANOVA + Tukey HSD + Bonferroni + Cohen's d
        ↓
03_visualize.py           ← heatmap, speedup chart, decision matrix
```

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Cara Pakai

### Step 1 — Validasi Data

```bash
python 01_validate_data.py ../benchmark-project/results/jmh_result_TIMESTAMP.csv
```

Output:
- `results/clean_data.csv` — data bersih (outlier removed)

Cek 5 hal:
1. **Completeness** — semua 120 runs terkumpul
2. **Consistency** — tidak ada score ≤ 0 atau kontradiksi
3. **Validity** — unit ns/op dan ops/s benar
4. **Representativeness** — scaling ArrayList O(n), HashMap O(1)
5. **Outlier** — deteksi |z| > 3

---

### Step 2 — Analisis Statistik

```bash
python 02_statistical_analysis.py ../benchmark-project/results/clean_data.csv
```

Output:
- `descriptive_stats.csv` — mean, median, std, CI 99%
- `anova_results.csv`     — Two-way ANOVA table
- `pairwise_comparison.csv` — Tukey HSD + Bonferroni
- `effect_sizes.csv`      — Cohen's d per kombinasi

Analisis sesuai proposal:
- α = 0.05, Bonferroni-corrected α = 0.05/20 = **0.0025**
- Cohen's d: medium > 0.5, large > 0.8
- Shapiro-Wilk (normalitas) + Levene (homogeneity)

---

### Step 3 — Visualisasi

```bash
python 03_visualize.py ../benchmark-project/results/
```

Output:
- `fig_execution_time.png`   — heatmap ns/op
- `fig_speedup_ratio.png`    — speedup HashMap vs ArrayList
- `fig_memory_footprint.png` — memory bytes per element
- `fig_decision_matrix.png`  — **decision matrix untuk developer**
- `decision_matrix.csv`      — tabel rekomendasi

---

## Interpretasi Hasil

Sesuai proposal E.5:

> Jika ANOVA menunjukkan **p < 0.0025** (Bonferroni-corrected) dan
> **Cohen's d > 0.5** untuk perbandingan ArrayList vs HashMap pada operasi search,
> maka: HashMap signifikan lebih cepat di search →
> **Gunakan HashMap untuk operasi search-heavy.**

### Hipotesis yang diuji:

| Hipotesis | Kondisi |
|-----------|---------|
| H₁a: HashMap lebih cepat di search | p < 0.0025 AND d > 0.8 |
| H₁b: ArrayList lebih cepat di iterate | p < 0.0025 AND d > 0.5 |
| H₁c: ArrayList lebih hemat memori (<10⁴) | diff > 10% |
