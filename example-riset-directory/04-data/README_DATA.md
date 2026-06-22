# 04-data — Data Mentah Hasil Benchmark

Folder ini berisi data mentah hasil eksekusi benchmark JMH dan memory profiling JOL.

---

## Struktur Data

### 1. JMH Benchmark Results

**File:** `results.csv` (dari `benchmark-project/results/results.csv`)

**Kolom:**
| Kolom | Tipe | Keterangan |
|---|---|---|
| `Benchmark` | String | Nama class + method (e.g., `ArrayListBenchmark.search`) |
| `Param:datasetSize` | Integer | Ukuran dataset (1000, 10000, 100000, 1000000) |
| `Mode` | String | avgt (average time) atau thrpt (throughput) |
| `Score` | Float | Nilai metrik (ns/op atau ops/s) |
| `Score Error` | Float | Margin of error (CI 99%) |
| `Units` | String | ns/op atau ops/s |

**Jumlah data:**
- 2 struktur data × 5 operasi × 4 ukuran dataset = **40 kombinasi**
- Setiap kombinasi: 3 forks × 10 iterations = **30 data points**
- **Total:** 40 × 30 = **1200 measurements**

**Contoh:**
```csv
Benchmark,Param:datasetSize,Mode,Score,Score Error,Units
ArrayListBenchmark.insert,1000,avgt,20.8,0.79,ns/op
ArrayListBenchmark.insert,10000,avgt,21.3,0.92,ns/op
HashMapBenchmark.search,1000,avgt,14.47,1.36,ns/op
```

### 2. Memory Footprint

**File:** `memory_footprint.csv` (dari `benchmark-project/results/memory_footprint.csv`)

**Kolom:**
| Kolom | Tipe | Keterangan |
|---|---|---|
| `data_structure` | String | ArrayList atau HashMap |
| `dataset_size` | Integer | Ukuran dataset (1000, 10000, 100000, 1000000) |
| `shallow_bytes` | Long | Ukuran objek sendiri (tanpa referensi) |
| `deep_bytes` | Long | Total termasuk semua referensi (Person objects) |
| `bytes_per_element` | Float | deep_bytes / dataset_size |

**Contoh:**
```csv
data_structure,dataset_size,shallow_bytes,deep_bytes,bytes_per_element
ArrayList,1000,16,40016,40.016
HashMap,1000,120,80120,80.12
```

---

## Validasi Data

### Outlier Detection

Outlier dideteksi menggunakan **Z-score** dengan threshold |z| > 3:

```python
z_score = (x - mean) / std
outlier = |z_score| > 3
```

**Hasil:** Tidak ada outlier ekstrem pada data bersih (semua Z-score < 3).

### Data Quality

**Kriteria clean data:**
- Coefficient of variation (CV) < 50% untuk mayoritas kombinasi
- Confidence interval 99% tidak overlap dengan 0
- Minimal 30 data points per kombinasi (power analysis target: 0.8)

**Hasil:** Semua kombinasi memenuhi kriteria clean data.

---

## Reproduksi Data

Untuk mereproduksi data mentah:

```bash
cd ../benchmark-project

# 1. Build benchmark JAR
mvn clean package

# 2. Run memory profiler (JOL)
java -cp target/benchmarks.jar \
    com.research.benchmark.MemoryProfiler \
    > results/memory_footprint.csv

# 3. Run JMH benchmark (full matrix)
java -jar target/benchmarks.jar \
    -rf csv \
    -rff results/results.csv

# Estimasi waktu: 2-4 jam (tergantung hardware)
```

---

## Metadata

| Atribut | Nilai |
|---|---|
| **Dataset generation** | seed=42 (reproducible) |
| **JVM** | Java 17 LTS (Oracle/Adoptium) |
| **GC** | G1GC (default Java 17) |
| **Heap** | 4GB fixed (`-Xms4g -Xmx4g`) |
| **Warmup** | 5 iterations × 1 second |
| **Measurement** | 10 iterations × 1 second |
| **Forks** | 3 (3 JVM instances terpisah) |
| **Total runs** | 40 kombinasi × 3 forks = **120 runs** |
| **Total measurements** | 120 runs × 10 iterations = **1200 data points** |
| **Waktu eksekusi** | ~2-4 jam |

---



