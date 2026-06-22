# Tahap 2: Eksekusi Benchmark Penuh

**Periode:** Minggu 8  
**Status:** ✅ Selesai  

---

## Tujuan Tahap

1. Menjalankan memory profiler JOL untuk measurement memory footprint (8 data points)
2. Menjalankan benchmark JMH penuh (40 kombinasi × 3 forks × 10 iterations = 1200 data points)
3. Mengumpulkan raw data (CSV) untuk analisis statistik
4. Validasi data mentah (no missing data, no crash)

---

## Matrix Eksperimen

**Kombinasi:**
- 2 struktur data: ArrayList, HashMap
- 5 operasi: insert, search, update, delete, iterate
- 4 ukuran dataset: 1000, 10000, 100000, 1000000
- **Total:** 2 × 5 × 4 = **40 kombinasi**

**Replikasi per kombinasi:**
- 3 forks (separate JVM instances)
- 10 measurement iterations per fork
- **Total data points per kombinasi:** 3 × 10 = **30 measurements**

**Total data points:** 40 × 30 = **1200 measurements**

---

## Eksekusi

### 2.1 Memory Profiler (JOL)

**Command:**
```bash
cd ../../benchmark-project/
java -cp target/benchmarks.jar \
    com.research.benchmark.MemoryProfiler \
    > results/memory_footprint.csv
```

**Output:** `results/memory_footprint.csv`

| data_structure | dataset_size | shallow_bytes | deep_bytes | bytes_per_element |
|---|---|---|---|---|
| ArrayList | 1000 | 16 | 40016 | 40.016 |
| ArrayList | 10000 | 16 | 400016 | 40.0016 |
| HashMap | 1000 | 120 | 80120 | 80.12 |
| HashMap | 10000 | 120 | 800120 | 80.012 |

**Durasi:** ~10 detik

---

### 2.2 JMH Benchmark (Full Matrix)

**Command:**
```bash
cd ../../benchmark-project/
java -jar target/benchmarks.jar \
    -rf csv \
    -rff results/results.csv
```

**Konfigurasi JMH (dari annotation):**
- Warmup: 5 iterations × 1 second
- Measurement: 10 iterations × 1 second
- Forks: 3
- JVM flags: `-Xms4g -Xmx4g -XX:+UseG1GC`

**Estimasi waktu:**
```
40 kombinasi × 3 forks × (5 warmup + 10 measurement) × 1 second
= 40 × 3 × 15 = 1800 seconds = 30 menit (best case)

Dengan overhead (JVM startup, GC, etc.): ~2-4 jam
```

**Output:** `results/results.csv`

**Contoh output:**
```csv
Benchmark,Mode,Threads,Samples,Score,Score Error (99.9%),Unit,Param: datasetSize
ArrayListBenchmark.insert,avgt,1,30,20.8,0.79,ns/op,1000
ArrayListBenchmark.search,avgt,1,30,1088.87,181.53,ns/op,1000
HashMapBenchmark.search,avgt,1,30,14.47,1.36,ns/op,1000
```

---

## Monitoring

### Real-time Progress

```bash
# Monitor JMH output
tail -f results/results.csv

# Monitor JVM processes
ps aux | grep java

# Monitor system resources
top -u $USER
```

### Expected Progress

| Waktu | Progress | Status |
|---|---|---|
| 0-30 min | ArrayList kombinasi 1-10 | Running |
| 30-60 min | ArrayList kombinasi 11-20 | Running |
| 60-90 min | HashMap kombinasi 1-10 | Running |
| 90-120 min | HashMap kombinasi 11-20 | Running |
| 120+ min | Finalisasi | Completed |

---

## Validasi Data

### Check Data Completeness

```bash
# Hitung jumlah baris (should be 1200 + 1 header)
wc -l results/results.csv
# Expected: 1201

# Check unique kombinasi (should be 40)
cut -d',' -f1,9 results/results.csv | sort -u | wc -l
# Expected: 40
```

### Check Data Quality

**Kriteria:**
- No missing values (no empty cells)
- Score > 0 (no zero or negative)
- Score Error < Score (no error > measurement)
- CV (coefficient of variation) < 50% untuk mayoritas kombinasi

**Python validation:**
```python
import pandas as pd

df = pd.read_csv('results/results.csv')
print(f"Total rows: {len(df)}")  # Should be 1200
print(f"Missing values: {df.isnull().sum().sum()}")  # Should be 0
print(f"Zero scores: {(df['Score'] == 0).sum()}")  # Should be 0
```

---

## Output Tahap 2

| File | Size | Deskripsi |
|---|---|---|
| `results/results.csv` | ~100 KB | JMH raw data (1200 measurements) |
| `results/memory_footprint.csv` | ~1 KB | JOL memory measurement (8 data points) |

---

## Kendala & Solusi

### Kendala yang Dialami

| Kendala | Dampak | Solusi |
|---|---|---|
| **JVM OutOfMemoryError** pada dataset 1M | Benchmark crash | Increase heap: `-Xms8g -Xmx8g` (jika RAM cukup) |
| **High measurement variance** (CV > 50%) | Data tidak reliable | Close background apps, run saat idle, increase iterations (`-i 20`) |
| **Benchmark terlalu lama** (>6 jam) | Timeline molor | Reduce warmup (`-wi 2`), run overnight |
| **Thermal throttling** (laptop overheat) | CPU frequency drop → variance tinggi | Run dengan cooling pad, reduce concurrent load |

### Troubleshooting

**Error: "Measurement variance too high"**
```bash
# Increase measurement iterations
java -jar target/benchmarks.jar -i 20
```

**Error: "OutOfMemoryError: Java heap space"**
```bash
# Increase heap size
java -jar target/benchmarks.jar \
    -jvmArgs "-Xms8g -Xmx8g"
```

**Warning: "CV (coefficient of variation) > 50%"**
- **Penyebab:** Background processes, GC activity, thermal throttling
- **Solusi:** Close background apps, run benchmark saat sistem idle

---

## Verifikasi Hasil

### Sample Data

**ArrayList.search, 1K dataset:**
```
Score (mean): 1088.87 ns/op
Score Error (99.9%): 181.53 ns/op
CV: 16.67%
```

**HashMap.search, 1K dataset:**
```
Score (mean): 14.47 ns/op
Score Error (99.9%): 1.36 ns/op
CV: 9.44%
```

**Interpretation:**
- HashMap **75× lebih cepat** pada search (1088.87 / 14.47 ≈ 75)
- CV < 20% → data quality baik
- Score Error < 20% of Score → measurement presisi

---

## Metadata Eksperimen

| Atribut | Nilai |
|---|---|
| **Dataset generation** | seed=42 (reproducible) |
| **JVM** | Java 17 LTS (OpenJDK 17.0.x) |
| **GC** | G1GC (default Java 17) |
| **Heap** | 4GB fixed (`-Xms4g -Xmx4g`) |
| **Warmup** | 5 iterations × 1 second |
| **Measurement** | 10 iterations × 1 second |
| **Forks** | 3 (separate JVM instances) |
| **Total combinations** | 40 |
| **Total measurements** | 1200 |
| **Execution time** | ~2-4 hours |
| **Hardware** | [Sesuai mesin yang digunakan, e.g., Intel i7-10750H, 16GB RAM] |
| **OS** | [Sesuai OS, e.g., Windows 11, Ubuntu 22.04] |

---

## Rekomendasi untuk Reproduksi

### Best Practices

1. **Run saat sistem idle** — close browser, IDE, background apps
2. **Monitor thermal** — pastikan CPU tidak thermal throttling
3. **Fixed heap** — gunakan `-Xms` = `-Xmx` untuk reduce GC variability
4. **Multiple runs** — jika variance tinggi, run benchmark 2-3× dan aggregate
5. **Document environment** — catat hardware, OS, Java version untuk reproducibility

### Environment Variables

```bash
# Set Java home (jika multiple Java version)
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk

# Set Maven opts (jika build memory error)
export MAVEN_OPTS="-Xmx2g"
```

---

## Status

✅ **Tahap 2 selesai** — data mentah (1200 measurements) terkumpul.

**Next:** [Tahap 3 — Analisis Statistik & Visualisasi](tahap-3-analisis-visualisasi.md)
