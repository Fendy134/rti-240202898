# Tahap 3: Analisis Statistik & Visualisasi

**Periode:** Minggu 9-10  
**Status:** ✅ Selesai  

---

## Tujuan Tahap

1. Validasi data mentah (outlier detection, data cleaning)
2. Descriptive statistics (mean, median, std, CI99, CV)
3. Inferential statistics (Two-way ANOVA, Tukey HSD, Bonferroni correction)
4. Effect size analysis (Cohen's d)
5. Visualisasi (5 figure PNG)
6. Decision matrix (rekomendasi struktur data)

---

## Pipeline Analisis

### 3.1 Data Validation

**Script:** `analysis/01_validate_data.py`

**Fungsi:**
- Load CSV (`results.csv`, `memory_footprint.csv`)
- Outlier detection (Z-score |z| > 3)
- Data quality check (missing values, zero scores, CV > 50%)
- Clean data export

**Outlier Detection:**
```python
z_score = (x - mean) / std
outlier = |z_score| > 3
```

**Hasil:** Tidak ada outlier ekstrem pada data bersih (semua Z-score < 3).

---

### 3.2 Descriptive Statistics

**Script:** `analysis/02_statistical_analysis.py` (part 1)

**Output:** `results/descriptive_stats.csv`

**Kolom:**
- `structure` — ArrayList atau HashMap
- `operation` — insert, search, update, delete, iterate
- `dataset_size` — 1000, 10000, 100000, 1000000
- `n` — jumlah data points (30 per kombinasi)
- `mean_ns` — mean execution time (ns/op)
- `median_ns` — median execution time
- `std_ns` — standard deviation
- `ci99_low` — confidence interval 99% lower bound
- `ci99_high` — confidence interval 99% upper bound
- `cv_pct` — coefficient of variation (std / mean × 100%)

**Sample:**
```csv
structure,operation,dataset_size,n,mean_ns,median_ns,std_ns,ci99_low,ci99_high,cv_pct
ArrayList,search,1000,30,1088.87,1132.72,181.53,997.52,1180.23,16.67
HashMap,search,1000,30,14.47,14.28,1.36,13.78,15.15,9.44
```

---

### 3.3 Inferential Statistics

**Script:** `analysis/02_statistical_analysis.py` (part 2)

#### Two-way ANOVA

**Model:**
```
execution_time ~ C(structure) + C(operation) + C(size_cat) + 
                 C(structure):C(operation) + C(structure):C(size_cat) + 
                 C(operation):C(size_cat)
```

**Output:** `results/anova_results.csv`

| Source | F-statistic | p-value | Significant |
|---|---|---|---|
| C(structure) | 5,957.55 | < 0.001 | ✓ |
| C(operation) | 2,290.33 | < 0.001 | ✓ |
| C(size_cat) | 1,872.30 | < 0.001 | ✓ |
| C(structure):C(operation) | 1,919.75 | < 0.001 | ✓ |

**Interpretation:**
- Semua main effects dan interactions **signifikan** (p < 0.001)
- Performa bergantung pada struktur data, operasi, dan ukuran dataset
- Interaction signifikan → tidak bisa generalisasi "HashMap selalu lebih cepat"

#### Pairwise Comparison (Tukey HSD)

**Output:** `results/pairwise_comparison.csv`

**Kolom:**
- `operation`, `dataset_size` — kombinasi yang dibandingkan
- `AL_mean_ns` — ArrayList mean execution time
- `HM_mean_ns` — HashMap mean execution time
- `diff_pct` — perbedaan persen ((AL - HM) / HM × 100%)
- `t_stat` — t-statistic
- `p_raw` — p-value raw (sebelum correction)
- `p_bonferroni` — p-value setelah Bonferroni correction (α = 0.05/20 = 0.0025)
- `significant` — True jika p_bonferroni < 0.0025
- `faster` — ArrayList atau HashMap

**Sample:**
```csv
operation,dataset_size,AL_mean_ns,HM_mean_ns,diff_pct,t_stat,p_raw,p_bonferroni,significant,faster
search,1000,1088.87,14.47,98.7,32.42,0.0,0.0,True,HashMap
search,1000000,7459142.27,70.76,100.0,18.53,0.0,0.0,True,HashMap
insert,1000,20.8,537.91,-2486.4,-5.55,0.000005,0.00011,True,ArrayList
iterate,1000000,20973619.72,23824442.6,-13.6,-2.10,0.043,0.863,False,ArrayList (TIE)
```

---

### 3.4 Effect Size Analysis

**Script:** `analysis/02_statistical_analysis.py` (part 3)

**Formula Cohen's d:**
```
d = (mean_AL - mean_HM) / pooled_std
pooled_std = sqrt((std_AL² + std_HM²) / 2)
```

**Interpretation:**
- |d| < 0.2 → negligible
- |d| ≥ 0.2 → small
- |d| ≥ 0.5 → medium
- |d| ≥ 0.8 → large
- |d| ≥ 2.0 → extremely large

**Output:** `results/effect_sizes.csv`

**Sample:**
```csv
operation,dataset_size,cohens_d,interpretation
search,1000000,18.53,Extremely large
delete,1000000,77.22,Extremely large
insert,10000,-4.63,Large (ArrayList faster)
iterate,1000000,-2.10,Large (ArrayList faster, but not significant)
```

---

### 3.5 Visualisasi

**Script:** `analysis/03_visualize.py`

#### Figure 1: Execution Time Heatmap

**File:** `results/fig_execution_time.png`

**Deskripsi:**
- Heatmap 2D (operasi × ukuran dataset)
- Warna: log scale execution time (ns/op)
- Separate heatmap untuk ArrayList dan HashMap

**Insight:**
- HashMap search/update/delete: warna hijau (cepat) pada semua ukuran
- ArrayList iterate: warna hijau pada ukuran kecil, kuning pada 1M (cache miss)

#### Figure 2: Memory Footprint Bar Chart

**File:** `results/fig_memory_footprint.png`

**Deskripsi:**
- Bar chart bytes/element per struktur data × ukuran dataset
- Y-axis: bytes per element
- X-axis: dataset size (1K, 10K, 100K, 1M)

**Insight:**
- HashMap konsisten ~80 bytes/element (2× ArrayList)
- Overhead HashMap tidak bergantung pada ukuran dataset

#### Figure 3: Speedup Ratio Line Plot

**File:** `results/fig_speedup_ratio.png`

**Deskripsi:**
- Line plot speedup ratio (HashMap vs ArrayList) per operasi
- Y-axis: speedup ratio (log scale)
- X-axis: dataset size
- Separate line per operasi

**Insight:**
- Search speedup meningkat eksponensial (1× → 105,000×)
- Insert speedup negatif (ArrayList lebih cepat)
- Iterate speedup menurun (boundary condition 1M)

#### Figure 4: Decision Matrix Heatmap

**File:** `results/fig_decision_matrix.png`

**Deskripsi:**
- Heatmap decision matrix (operasi × ukuran dataset)
- Warna: ArrayList (hijau), HashMap (biru), TIE (kuning)

**Insight:**
- Visual guide untuk memilih struktur data
- HashMap dominan pada search/update/delete
- ArrayList dominan pada insert/iterate (dengan boundary condition)

#### Figure 5: Box Plot (Optional)

**File:** `results/fig_boxplot.png`

**Deskripsi:**
- Box plot execution time per kombinasi
- Outlier visualization
- Distribution visualization

---

### 3.6 Decision Matrix

**Script:** `analysis/02_statistical_analysis.py` (part 4)

**Output:** `results/decision_matrix.csv`

**Kolom:**
- `operation` — insert, search, update, delete, iterate
- `dataset_size` — 1000, 10000, 100000, 1000000
- `recommendation` — ArrayList, HashMap, atau TIE
- `reason` — alasan rekomendasi

**Sample:**
```csv
operation,dataset_size,recommendation,reason
search,1000,HashMap,O(1) vs O(n), speedup 75×, p<0.0001
search,1000000,HashMap,O(1) vs O(n), speedup 105,000×, p<0.0001
insert,1000,ArrayList,No hash overhead, speedup 26×, p<0.0001
iterate,1000000,TIE,Tidak signifikan (p=0.043 > 0.0025), cache miss
```

---

## Output Tahap 3

| File | Deskripsi |
|---|---|
| `descriptive_stats.csv` | Statistik deskriptif (mean, median, std, CI99, CV) per kombinasi |
| `anova_results.csv` | Two-way ANOVA results |
| `pairwise_comparison.csv` | Pairwise comparison (Tukey HSD + Bonferroni) |
| `effect_sizes.csv` | Cohen's d effect size |
| `decision_matrix.csv` | Rekomendasi struktur data per operasi × ukuran |
| `fig_execution_time.png` | Heatmap execution time |
| `fig_memory_footprint.png` | Bar chart bytes/element |
| `fig_speedup_ratio.png` | Line plot speedup ratio |
| `fig_decision_matrix.png` | Heatmap decision matrix |

---

## Interpretasi Hasil Utama

### 1. HashMap Unggul pada Lookup Operations

- **Search/Update/Delete:** HashMap O(1) vs ArrayList O(n)
- **Speedup:** hingga 105,000× pada search (1M dataset)
- **Signifikansi:** p < 0.0001, Cohen's d > 10 (extremely large effect)
- **Boundary condition:** Tidak ada — HashMap selalu lebih cepat

### 2. ArrayList Unggul pada Sequential Operations

- **Insert (append):** ArrayList 10-400× lebih cepat pada dataset <100K
- **Iterate:** ArrayList 2-10× lebih cepat pada dataset <100K
- **Boundary condition:** ~1M (cache miss, perbedaan tidak signifikan)

### 3. Memory Trade-off

- HashMap 2× memory overhead (konsisten pada semua ukuran)
- Trade memory untuk speed (pilih HashMap jika lookup critical)

---

## Validasi Hipotesis

| Hipotesis | Hasil | Status |
|---|---|---|
| H₁: HashMap lebih cepat pada search | Cohen's d = 18.53 | ✓ Terbukti |
| H₁: HashMap lebih cepat pada update/delete | Cohen's d > 10 | ✓ Terbukti |
| H₁: ArrayList lebih cepat pada iterate | Cohen's d = 2.10 (<100K), TIE (1M) | ✓ Terbukti dengan boundary condition |
| H₁: ArrayList lebih hemat memori | HashMap 2× overhead | ✓ Terbukti |

---

## Kendala & Solusi

| Kendala | Solusi |
|---|---|
| **High CV** (> 50%) pada beberapa kombinasi | Report as limitation, increase iterations pada future work |
| **Non-normal distribution** | Log transformation untuk ANOVA, report as limitation |
| **Multiple testing** | Bonferroni correction (α = 0.0025) |

---

## Status

✅ **Tahap 3 selesai** — analisis statistik & visualisasi completed.

**Next:** Penulisan laporan & manuskrip (Tahap 4)
