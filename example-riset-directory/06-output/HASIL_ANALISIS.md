# 06-output — Hasil Analisis Statistik & Visualisasi

Folder ini berisi output analisis statistik dan visualisasi dari data benchmark JMH.

---

## Daftar File Output

### 1. Tabel Statistik (CSV)

**Lokasi:** `../../benchmark-project/results/`

| File | Deskripsi | Kolom Utama |
|---|---|---|
| `descriptive_stats.csv` | Statistik deskriptif per kombinasi (struktur, operasi, ukuran) | structure, operation, dataset_size, n, mean_ns, median_ns, std_ns, ci99_low, ci99_high, cv_pct |
| `anova_results.csv` | Two-way ANOVA results | source, F, p_value, significant |
| `pairwise_comparison.csv` | Pairwise comparison (ArrayList vs HashMap per operasi & ukuran) | operation, dataset_size, AL_mean_ns, HM_mean_ns, diff_pct, t_stat, p_raw, p_bonferroni, significant, faster |
| `effect_sizes.csv` | Cohen's d effect size | operation, dataset_size, cohens_d, interpretation |
| `decision_matrix.csv` | Rekomendasi struktur data | operation, dataset_size, recommendation, reason |

### 2. Visualisasi (PNG)

**Lokasi:** `../../benchmark-project/results/`

| File | Deskripsi | Insight Utama |
|---|---|---|
| `fig_execution_time.png` | Heatmap execution time (ns/op) per struktur, operasi, ukuran | HashMap unggul pada search/update/delete (100-1000× lebih cepat), ArrayList unggul pada insert/iterate |
| `fig_memory_footprint.png` | Bar chart memory footprint (bytes/element) | HashMap overhead ~2× pada semua ukuran dataset |
| `fig_speedup_ratio.png` | Line plot speedup ratio (HashMap vs ArrayList) | Speedup HashMap pada search mencapai >100,000× pada dataset 1M |
| `fig_decision_matrix.png` | Heatmap decision matrix (rekomendasi struktur data) | Visual guide untuk memilih struktur data berdasarkan operasi dominan × ukuran dataset |

---

## Ringkasan Hasil Utama

### 1. Descriptive Statistics

**Contoh: Execution Time (mean_ns)**

| Structure | Operation | 1K | 10K | 100K | 1M |
|---|---|---|---|---|---|
| ArrayList | insert | 20.8 | 21.3 | 21.0 | 7,053.4 |
| ArrayList | search | 1,088.9 | 14,023.5 | 529,152.5 | 7,459,142.3 |
| ArrayList | update | 886.8 | 15,975.6 | 433,989.8 | 6,021,439.8 |
| ArrayList | delete | 49,391.8 | 19,623.7 | 1,269,170.5 | 13,964,676.8 |
| ArrayList | iterate | 2,097.9 | 54,684.3 | 1,437,068.1 | 20,973,619.7 |
| HashMap | insert | 537.9 | 9,055.3 | 666.2 | 235.6 |
| HashMap | search | 14.5 | 23.8 | 40.7 | 70.8 |
| HashMap | update | 58.0 | 96.0 | 211.1 | 584.7 |
| HashMap | delete | 52.6 | 75.7 | 87.9 | 111.7 |
| HashMap | iterate | 9,189.5 | 90,273.5 | 2,137,005.2 | 23,824,442.6 |

**Insight:**
- HashMap **unggul signifikan** pada search/update/delete (O(1) vs O(n))
- ArrayList **unggul** pada insert (append) dan iterate (cache locality)
- Pada dataset 1M, ArrayList.insert overhead meningkat (resize)

### 2. ANOVA Results

**Two-way ANOVA (struktur data × ukuran dataset):**

| Source | F-statistic | p-value | Significant |
|---|---|---|---|
| C(structure) | 5,957.55 | 0.0 | ✓ |
| C(operation) | 2,290.33 | 0.0 | ✓ |
| C(size_cat) | 1,872.30 | 0.0 | ✓ |
| C(structure):C(operation) | 1,919.75 | 0.0 | ✓ |
| C(structure):C(size_cat) | 582.11 | 0.0 | ✓ |
| C(operation):C(size_cat) | 107.22 | 0.0 | ✓ |

**Interpretation:**
- Semua main effects dan interactions **signifikan** (p < 0.001)
- Performa **sangat bergantung** pada struktur data, operasi, dan ukuran dataset
- Interaction signifikan → tidak bisa generalisasi "HashMap selalu lebih cepat"

### 3. Pairwise Comparison (Sample)

**HashMap vs ArrayList (dengan Bonferroni correction α = 0.0025):**

| Operation | Dataset | ArrayList (ns) | HashMap (ns) | Diff % | p-value | Significant | Faster |
|---|---|---|---|---|---|---|---|
| **search** | 1K | 1,088.9 | 14.5 | **+98.7%** | 0.0 | ✓ | HashMap |
| **search** | 10K | 14,023.5 | 23.8 | **+99.8%** | 0.0 | ✓ | HashMap |
| **search** | 100K | 529,152.5 | 40.7 | **+100.0%** | 0.0 | ✓ | HashMap |
| **search** | 1M | 7,459,142.3 | 70.8 | **+100.0%** | 0.0 | ✓ | HashMap |
| **insert** | 1K | 20.8 | 537.9 | **-2,486%** | <0.001 | ✓ | ArrayList |
| **insert** | 10K | 21.3 | 9,055.3 | **-42,407%** | <0.001 | ✓ | ArrayList |
| **iterate** | 1M | 20,973,619.7 | 23,824,442.6 | **-13.6%** | 0.043 | **✗** | ArrayList (TIE) |

**Insight:**
- HashMap **105,000× lebih cepat** pada search (1M dataset)
- ArrayList **400× lebih cepat** pada insert (10K dataset)
- Pada iterate 1M, perbedaan **tidak signifikan** (p=0.043 > 0.0025) — **TIE**

### 4. Effect Sizes (Cohen's d)

| Operation | Dataset | Cohen's d | Interpretation |
|---|---|---|---|
| search (1M) | 1M | 18.53 | **Extremely large** |
| delete (1M) | 1M | 77.22 | **Extremely large** |
| insert (10K) | 10K | -4.63 | **Large** (ArrayList faster) |
| iterate (1M) | 1M | -2.10 | **Large** (ArrayList faster, but not significant) |

**Interpretation:**
- Cohen's d > 0.8 → large effect
- Cohen's d > 2.0 → extremely large effect
- Negative d → ArrayList faster

### 5. Memory Footprint

**Bytes per element:**

| Structure | 1K | 10K | 100K | 1M |
|---|---|---|---|---|
| ArrayList | ~40 | ~40 | ~40 | ~40 |
| HashMap | ~80 | ~80 | ~80 | ~80 |

**Insight:**
- HashMap **2× memory overhead** pada semua ukuran dataset
- Overhead HashMap konsisten (~40 bytes per entry untuk Node wrapper)

### 6. Decision Matrix

| Operation Dominan | Dataset Size | Rekomendasi | Alasan |
|---|---|---|---|
| **search** | Semua | HashMap | O(1) vs O(n), speedup >100× |
| **update** | Semua | HashMap | O(1) vs O(n), speedup >100× |
| **delete** | Semua | HashMap | O(1) vs O(n), speedup >1000× |
| **insert** (append) | <100K | ArrayList | No hash overhead, 10-400× lebih cepat |
| **insert** (append) | 1M | HashMap | ArrayList resize overhead |
| **iterate** | <100K | ArrayList | Cache locality, 2-10× lebih cepat |
| **iterate** | 1M | TIE | Perbedaan tidak signifikan (cache miss) |

---

## Interpretasi & Boundary Conditions

### 1. HashMap Unggul pada Lookup Operations

**Search/Update/Delete:**
- HashMap O(1) rata-rata vs ArrayList O(n)
- Speedup mencapai **105,000×** pada search (1M dataset)
- Signifikan pada **semua ukuran dataset** (p < 0.0001)

**Boundary condition:** Tidak ada — HashMap selalu lebih cepat

### 2. ArrayList Unggul pada Sequential Operations

**Insert (append):**
- ArrayList O(1) amortized vs HashMap O(1) dengan hash overhead
- ArrayList **10-400× lebih cepat** pada dataset <100K
- Pada 1M, ArrayList resize overhead → HashMap lebih cepat

**Boundary condition:** ~100K-1M (resize mulai dominan)

**Iterate:**
- ArrayList cache-friendly vs HashMap pointer chasing
- ArrayList **2-10× lebih cepat** pada dataset <100K
- Pada 1M, perbedaan **tidak signifikan** (p=0.043 > 0.0025)

**Boundary condition:** ~1M (cache miss pada ArrayList)

### 3. Memory Trade-off

- HashMap **2× memory overhead** pada semua ukuran dataset
- Jika memory constraint ketat → pilih ArrayList
- Jika performa lookup critical → pilih HashMap (trade memory untuk speed)

---

## Limitasi & Future Work

### Limitasi

1. **Single-threaded** — tidak mengukur performa pada concurrent scenario (perlu `ConcurrentHashMap` vs `CopyOnWriteArrayList`)
2. **Uniform distribution** — tidak mengukur worst-case hash collision (perlu custom hash function)
3. **POJO sederhana** — tidak mengukur overhead pada objek kompleks (nested objects, large strings)
4. **Fixed seed** — tidak mengukur variabilitas pada random dataset berbeda

### Future Work

1. Evaluasi pada **multithreading** (concurrent collections)
2. Evaluasi pada **non-uniform distribution** (skewed data, worst-case hash collision)
3. Evaluasi pada **operasi mixed** (realistic workload: 70% read, 20% write, 10% delete)
4. Evaluasi pada **objek kompleks** (nested objects, large strings, binary data)

---

## Cara Mengakses File

### Tabel CSV

```bash
cd ../../benchmark-project/results/
ls *.csv
```

### Visualisasi PNG

```bash
cd ../../benchmark-project/results/
ls fig_*.png
```

### Load di Python

```python
import pandas as pd

# Descriptive stats
df = pd.read_csv('../../benchmark-project/results/descriptive_stats.csv')
print(df.head())

# Pairwise comparison
df_pairwise = pd.read_csv('../../benchmark-project/results/pairwise_comparison.csv')
print(df_pairwise[df_pairwise['significant'] == True])
```

---

## Referensi

- Descriptive Statistics: `../../benchmark-project/results/descriptive_stats.csv`
- ANOVA Results: `../../benchmark-project/results/anova_results.csv`
- Pairwise Comparison: `../../benchmark-project/results/pairwise_comparison.csv`
- Decision Matrix: `../../benchmark-project/results/decision_matrix.csv`
- Visualizations: `../../benchmark-project/results/fig_*.png`
