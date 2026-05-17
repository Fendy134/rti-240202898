# WS-06: System-Experiment Mapping

> **Bab 6 — System Design sebagai Experimental Artifact**

---

## Ringkasan Materi

### Sistem = Instrumen Pengujian, Bukan Produk

Seorang engineer bertanya "apakah sistem bekerja?" — seorang peneliti bertanya "apa yang bisa dibuktikan sistem ini?" Sistem dalam riset adalah **artifact** — objek yang sengaja dibuat untuk menguji klaim spesifik.

### System as Experiment Model

```
RQ → Variable → System Component → Experimental Setup → Output
```

Setiap komponen sistem harus bisa ditelusuri ke variabel riset (top-down), dan setiap pengukuran harus menjawab RQ (bottom-up).

### Mapping Variabel ke Komponen

| Tipe Variabel | Peran di Sistem | Contoh |
|---------------|----------------|--------|
| **IV** (Independent) | Modul yang bisa di-toggle/swap | Algoritma A vs B, struktur data ArrayList vs HashMap |
| **DV** (Dependent) | Modul pengukuran | Logger, metrics collector, JMH benchmark |
| **CV** (Control) | Config yang dikunci | Dataset, parameter tetap, JVM flags |

Jika variabel tidak bisa di-map ke komponen apapun → arsitektur perlu didesain ulang.

### 4 Prinsip Desain Eksperimental

| Prinsip | Pertanyaan Kunci |
|---------|------------------|
| **Traceability** | Komponen ini melayani variabel yang mana? |
| **Modularity** | Bisakah IV diubah tanpa memengaruhi yang lain? |
| **Controllability** | Apakah CV dieksternalisasi ke config file? |
| **Measurability** | Apakah sistem otomatis menghasilkan data yang dibutuhkan? |

### Variable Isolation melalui Arsitektur

- **Modular architecture** — Pisahkan berdasarkan variabel
- **Configuration-driven** — Ubah config (YAML/JSON), bukan code
- **Feature toggles** — On/off flag untuk ablation study

### Research vs Engineering

| Aspek | Engineering | Research |
|:------|:-----------|:----------|
| Tujuan sistem | Memenuhi kebutuhan user | Menguji hipotesis, menghasilkan bukti |
| Arsitektur | Optimasi performa & skalabilitas | Optimasi isolasi variabel & reprodusibilitas |
| Konfigurasi | Sering hardcoded | Dieksternalisasi ke config file |
| Fitur tambahan | Menambah nilai user | Menambah noise jika tidak terkait RQ |

### Istilah Penting

- **Artifact** — Objek yang sengaja dibuat untuk memecahkan masalah atau menguji proposisi
- **Traceability** — Kemampuan menelusuri hubungan RQ → variabel → komponen → output
- **Variable Isolation** — Mengubah hanya satu variabel sambil menahan yang lain konstan
- **Ablation Study** — Menguji kontribusi tiap komponen dengan melepasnya satu per satu
- **Configuration-driven Execution** — Semua parameter di config file, bukan hardcoded

---

# WS-06: System-Experiment Mapping
**Mata Kuliah:** Riset Teknologi Informasi

---

## SYSTEM-EXPERIMENT MAPPING

**Research Question:**  
Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara ArrayList<Person> dan HashMap<Integer, Person> pada 5 operasi CRUD dasar untuk 4 ukuran dataset (10³–10⁶) di Java 17 LTS?

---

### Variable → Component Mapping

| Variabel | Tipe | Komponen Sistem | Cara Manipulasi/Pengukuran |
|:---------|:----:|:-----------------|:---------------------------|
| **Struktur data** | IV | Modul koleksi (ArrayList vs HashMap) | Ganti config `data_structure: ["ArrayList", "HashMap"]` dan instantiate sesuai pilihan |
| **Jenis operasi** | IV | Modul operasi CRUD (5 benchmark methods) | Ganti config `operations: ["insert", "search", "update", "delete", "iterate"]` dan jalankan method yang sesuai |
| **Ukuran dataset** | IV | Modul data generator | Ganti config `dataset_sizes: [1000, 10000, 100000, 1000000]` dan generate dataset sesuai ukuran |
| **Execution time** | DV | Modul JMH benchmark | JMH otomatis mengukur dengan `@Benchmark`, output dalam ns/op dengan confidence interval 99% |
| **Memory footprint** | DV | Modul JOL memory profiler | JOL `GraphLayout.parseInstance().totalSize()` mengukur shallow + deep size dalam bytes |
| **Throughput** | DV | Modul JMH output processor | JMH otomatis menghitung ops/sec (inverse dari ns/op) |
| **JVM version** | CV | Environment variable | Dikunci di environment: `JAVA_HOME=/usr/lib/jvm/java-17-openjdk` |
| **GC algorithm** | CV | JVM flag | Dikunci di JVM flag: `-XX:+UseG1GC` |
| **Heap size** | CV | JVM flag | Dikunci di JVM flag: `-Xms4g -Xmx4g` |
| **Warmup iterations** | CV | JMH annotation | Dikunci di `@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)` |
| **Measurement iterations** | CV | JMH annotation | Dikunci di `@Measurement(iterations = 10, time = 1, timeUnit = TimeUnit.SECONDS)` |
| **Forks** | CV | JMH annotation | Dikunci di `@Fork(value = 3)` |

---

### 4 Prinsip Desain

**[X] Traceability** — Setiap komponen bisa ditelusuri ke variabel:
- ArrayList/HashMap modul → IV struktur data
- 5 benchmark methods → IV jenis operasi
- Data generator → IV ukuran dataset
- JMH/JOL → DV execution time/memory

**[X] Modularity** — IV bisa diubah tanpa mengubah CV:
- Ganti struktur data di config → tidak perlu ubah JVM flags
- Ganti operasi di config → tidak perlu ubah heap size
- Ganti ukuran dataset → tidak perlu ubah GC algorithm

**[X] Controllability** — CV dieksternalisasi ke config/environment:
- JVM version di environment variable
- GC algorithm di JVM flag
- Heap size di JVM flag
- Warmup/measurement/forks di JMH annotation (bukan hardcoded)

**[X] Measurability** — Pengukuran DV built-in di modul:
- JMH menghasilkan execution time otomatis
- JOL menghasilkan memory footprint otomatis
- Throughput dihitung dari execution time

---

### Experimental Setup

**Input data:**
- Dataset POJO `Person` (id: int, name: String, age: int, email: String)
- 4 ukuran: 10³, 10⁴, 10⁵, 10⁶ elemen
- Di-generate dengan `Random` ber-seed tetap (seed = 42) untuk reproducibility
- Distribusi: uniform random untuk id (0–1M), random string untuk name/email, random int untuk age (18–80)

**Parameter eksperimen:**
- `data_structure`: ArrayList, HashMap
- `operations`: insert, search, update, delete, iterate
- `dataset_sizes`: 1000, 10000, 100000, 1000000
- `jvm_version`: Java 17 LTS
- `gc_algorithm`: G1GC
- `heap_size`: 4GB fixed (`-Xms4g -Xmx4g`)
- `warmup_iterations`: 5 × 1 second
- `measurement_iterations`: 10 × 1 second
- `forks`: 3 (3 JVM instance terpisah)

**Output format:**
- CSV: `benchmark_results.csv` dengan columns: data_structure, operation, dataset_size, fork_id, iteration, execution_time_ns, memory_bytes, throughput_ops_sec, timestamp
- JSON: `benchmark_summary.json` dengan aggregated statistics: mean, median, std_dev, min, max, percentile_95, percentile_99, confidence_interval_99
- Log: `benchmark.log` dengan detailed JMH output dan GC events

---

### Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    JMH Benchmark Harness                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │  ArrayList       │  │  HashMap         │  ← IV       │
│  │  Benchmark       │  │  Benchmark       │             │
│  │  Methods         │  │  Methods         │             │
│  └──────────────────┘  └──────────────────┘             │
│         ↓                      ↓                          │
│  ┌──────────────────────────────────────┐               │
│  │  Data Generator (Seed = 42)          │  ← IV        │
│  │  - 10³, 10⁴, 10⁵, 10⁶ elemen        │               │
│  │  - POJO Person (id, name, age, email)│               │
│  └──────────────────────────────────────┘               │
│         ↓                                                 │
│  ┌──────────────────────────────────────┐               │
│  │  5 Operation Methods                 │  ← IV        │
│  │  - insert()                          │               │
│  │  - search()                          │               │
│  │  - update()                          │               │
│  │  - delete()                          │               │
│  │  - iterate()                         │               │
│  └──────────────────────────────────────┘               │
│         ↓                                                 │
│  ┌──────────────────────────────────────┐               │
│  │  Measurement Modules                 │  ← DV        │
│  │  - JMH Timer (ns/op)                 │               │
│  │  - JOL Memory Profiler (bytes)       │               │
│  │  - Throughput Calculator (ops/sec)   │               │
│  └──────────────────────────────────────┘               │
│         ↓                                                 │
│  ┌──────────────────────────────────────┐               │
│  │  Output Modules                      │               │
│  │  - CSV Writer                        │               │
│  │  - JSON Aggregator                   │               │
│  │  - Statistical Analyzer (ANOVA)      │               │
│  └──────────────────────────────────────┘               │
│                                                           │
│  ┌──────────────────────────────────────┐               │
│  │  Control Variables (CV)              │               │
│  │  - JVM: Java 17 LTS                  │               │
│  │  - GC: G1GC                          │               │
│  │  - Heap: 4GB fixed                   │               │
│  │  - Warmup: 5 × 1s                    │               │
│  │  - Measurement: 10 × 1s              │               │
│  │  - Forks: 3                          │               │
│  └──────────────────────────────────────┘               │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

# Latihan 1 — Variable-to-Component Mapping

**RQ:** Bagaimana perbedaan performa ArrayList vs HashMap pada 5 operasi CRUD untuk 4 ukuran dataset di Java 17?

| Variabel | Tipe | Komponen Sistem | Cara Manipulasi / Pengukuran |
|:---------|:----:|:-----------------|:---------------------------|
| Struktur data | IV | Modul ArrayList vs HashMap | Ganti config `data_structure` dan instantiate sesuai pilihan |
| Jenis operasi | IV | 5 benchmark methods (@Benchmark) | Ganti config `operations` dan jalankan method yang sesuai |
| Ukuran dataset | IV | Data generator dengan seed tetap | Ganti config `dataset_sizes` dan generate dataset sesuai ukuran |
| Execution time | DV | JMH timer | JMH otomatis mengukur ns/op dengan CI 99% |
| Memory footprint | DV | JOL memory profiler | JOL mengukur bytes via GraphLayout.parseInstance().totalSize() |
| Throughput | DV | JMH output processor | JMH menghitung ops/sec (inverse dari ns/op) |
| JVM version | CV | Environment variable | Dikunci di JAVA_HOME=/usr/lib/jvm/java-17-openjdk |
| GC algorithm | CV | JVM flag | Dikunci di -XX:+UseG1GC |
| Heap size | CV | JVM flag | Dikunci di -Xms4g -Xmx4g |

**Apakah semua variabel bisa di-map?** [X] Ya / [ ] Tidak

> Jika tidak, komponen apa yang perlu ditambahkan? Semua variabel sudah ter-map dengan jelas ke komponen sistem.

---

# Latihan 2 — 4 Prinsip Desain

**Evaluasi desain sistem terhadap 4 prinsip:**

| Prinsip | Status | Bukti / Penjelasan |
|:--------|:------:|:------------------|
| **Traceability** | ✅ | Setiap komponen (ArrayList/HashMap modul, 5 benchmark methods, data generator, JMH/JOL) bisa ditelusuri ke variabel riset (IV struktur data, IV operasi, IV ukuran, DV execution time/memory). |
| **Modularity** | ✅ | IV bisa diubah tanpa mengubah CV: ganti struktur data di config tidak perlu ubah JVM flags; ganti operasi tidak perlu ubah heap size; ganti ukuran dataset tidak perlu ubah GC algorithm. |
| **Controllability** | ✅ | CV dieksternalisasi ke config/environment: JVM version di environment variable, GC algorithm di JVM flag, heap size di JVM flag, warmup/measurement/forks di JMH annotation (bukan hardcoded di code). |
| **Measurability** | ✅ | Pengukuran DV built-in di modul: JMH menghasilkan execution time otomatis, JOL menghasilkan memory footprint otomatis, throughput dihitung dari execution time. Output format terstruktur (CSV, JSON) untuk analisis. |

**Prinsip mana yang paling sulit dipenuhi?** **Controllability** — karena JMH annotation tidak bisa di-override dari command line tanpa recompile.

**Strategi untuk mengatasinya:**
> Menggunakan JMH `@Fork` dengan parameter yang bisa di-override via system property, atau membuat wrapper script yang menggunakan JMH command-line options (`-wi`, `-i`, `-f`) untuk override annotation defaults tanpa recompile.

---

# Latihan 3 — Ablation Study Planning

**Jika sistem memiliki 3 komponen utama (ArrayList, HashMap, Data Generator), rencanakan ablation study:**

| Kondisi | ArrayList | HashMap | Data Generator | Hasil yang Diharapkan |
|:--------|:---------:|:-------:|:---------------:|:---------------------|
| **Full** | ✅ | ✅ | ✅ (seed=42) | Baseline penuh: perbandingan ArrayList vs HashMap pada data uniform random |
| **– ArrayList** | ❌ | ✅ | ✅ (seed=42) | Hanya HashMap: untuk memastikan HashMap berfungsi standalone |
| **– HashMap** | ✅ | ❌ | ✅ (seed=42) | Hanya ArrayList: untuk memastikan ArrayList berfungsi standalone |
| **– Data Generator** | ✅ | ✅ | ❌ (seed=0, empty) | Dengan dataset kosong: untuk mengukur overhead struktur data tanpa data |
| **Vary seed** | ✅ | ✅ | ✅ (seed=123) | Dengan seed berbeda: untuk memastikan hasil tidak bergantung pada seed tertentu |

**Komponen mana yang diprediksi paling berkontribusi?** **HashMap** — karena kompleksitas operasi search sangat berbeda (O(1) vs O(n)).

**Mengapa?**
> HashMap menggunakan hash table dengan O(1) average case lookup, sementara ArrayList menggunakan linear search O(n). Perbedaan ini akan sangat terlihat pada operasi search dengan dataset besar (10⁵–10⁶). Sebaliknya, untuk operasi insert dan iterate, perbedaan mungkin lebih kecil karena ArrayList append O(1) amortized dan HashMap juga O(1) average case.

---

# Refleksi

**Pertanyaan:** Apa risiko jika sistem dibangun seperti produk (monolitik, fitur lengkap) lalu baru dilakukan eksperimen? Mengapa arsitektur modular penting untuk riset?

**Jawaban:**

**Risiko jika sistem dibangun seperti produk (monolitik):**

1. **Sulit isolasi variabel** — Jika ArrayList dan HashMap di-hardcode dalam satu class, tidak bisa swap tanpa recompile. Jika operasi insert/search/update/delete di-hardcode dalam satu method, tidak bisa jalankan operasi tertentu saja.

2. **Sulit kontrol CV** — Jika JVM flags, heap size, GC algorithm di-hardcode atau di-set di constructor, tidak bisa ubah tanpa recompile. Jika warmup/measurement iterations di-hardcode di loop, tidak bisa ubah tanpa recompile.

3. **Sulit replikasi** — Jika parameter tersebar di berbagai tempat (hardcoded di code, di config file, di environment variable), sulit untuk orang lain mereplikasi eksperimen dengan parameter yang sama.

4. **Sulit ablation study** — Jika semua komponen tightly coupled, tidak bisa "matikan" satu komponen untuk melihat kontribusinya. Harus refactor besar-besaran.

5. **Sulit scale eksperimen** — Jika ingin menambah variabel baru (misal: Java 11, Java 21, berbagai GC algorithm), harus refactor code. Dengan modular architecture, cukup tambah config.

**Mengapa arsitektur modular penting untuk riset:**

1. **Reproducibility** — Dengan config-driven execution, orang lain bisa mereplikasi eksperimen dengan parameter yang sama hanya dengan mengubah config file, tanpa perlu memahami code.

2. **Scalability** — Mudah menambah variabel baru (IV, CV) tanpa refactor code. Contoh: ingin test Java 11 juga? Cukup tambah di config `java_versions: [11, 17, 21]`.

3. **Transparency** — Semua parameter terlihat di config file, tidak tersembunyi di code. Reviewer bisa dengan mudah melihat apa yang di-test dan bagaimana.

4. **Flexibility** — Mudah melakukan ablation study, sensitivity analysis, atau eksperimen tambahan tanpa refactor code.

5. **Collaboration** — Dengan modular architecture dan config-driven execution, tim bisa dengan mudah berkolaborasi: satu orang handle ArrayList modul, satu orang handle HashMap modul, satu orang handle data generator, tanpa conflict.

**Kesimpulan:**
Arsitektur modular bukan hanya tentang code quality, tapi tentang **scientific rigor**. Dengan modular architecture, riset menjadi lebih reproducible, transparent, dan scalable — yang adalah prinsip fundamental dalam scientific research.