# 05-kode — Source Code

Folder ini berisi referensi ke source code benchmark JMH dan analisis Python.

## Lokasi Source Code

Source code benchmark **tidak** disimpan di folder ini, melainkan di:

```
../../benchmark-project/
```

Lihat dokumentasi lengkap di: [README_KODE.md](README_KODE.md)

## Struktur Kode Benchmark

```
../../benchmark-project/
├── pom.xml                          ← Dependencies (JMH 1.37, JOL 0.17)
├── src/main/java/com/research/
│   ├── model/
│   │   └── Person.java              ← POJO data (id, name, age, email)
│   └── benchmark/
│       ├── DatasetGenerator.java    ← Generate dataset (seed=42)
│       ├── ArrayListBenchmark.java  ← 5 operasi CRUD ArrayList
│       ├── HashMapBenchmark.java    ← 5 operasi CRUD HashMap
│       └── MemoryProfiler.java      ← JOL memory measurement
└── results/                         ← Output benchmark (auto-created)
```

## Cara Menjalankan

Lihat dokumentasi lengkap: [../../benchmark-project/README.md](../../benchmark-project/README.md)

**Quick start:**

```bash
cd ../../benchmark-project/

# Build
mvn clean package

# Run memory profiler (JOL)
java -cp target/benchmarks.jar com.research.benchmark.MemoryProfiler \
    > results/memory_footprint.csv

# Run JMH benchmark (full matrix)
java -jar target/benchmarks.jar -rf csv -rff results/results.csv

# Estimasi waktu: 2-4 jam
```

## Analisis Python

Untuk analisis statistik, lihat:

```
../../analysis/
├── 01_validate_data.py          ← Load CSV, outlier detection
├── 02_statistical_analysis.py   ← ANOVA, Tukey HSD, Cohen's d
├── 03_visualize.py              ← 5 figure PNG
└── requirements.txt             ← pandas, scipy, matplotlib
```

Dokumentasi lengkap: [../../analysis/README.md](../../analysis/README.md)
