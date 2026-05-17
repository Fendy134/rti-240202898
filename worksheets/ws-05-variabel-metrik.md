# WS-05: Variabel & Metrik

> **Bab 5 — Metric, Measurement & Data**

---

## Ringkasan Materi

### Measurement Alignment Model

Setiap pengukuran yang valid harus bisa ditelusuri melalui rantai ini tanpa lompatan logis:

```
Problem → Concept → Variable → Metric → Data → Result
```

### Operationalization = Keputusan Desain

Menerjemahkan konsep abstrak menjadi variabel terukur bukan proses mekanis. "Code quality" yang diukur via SonarQube code smells membawa asumsi implisit. Setiap operasionalisasi harus didokumentasikan dan dijustifikasi.

### Empat Tipe Data (NOIR)

| Tipe | Ciri | Contoh | Operasi Valid |
|------|------|--------|---------------|
| **Nominal** | Kategori, tanpa urutan | Jenis algoritma (RF, SVM, CNN) | Modus, chi-square |
| **Ordinal** | Urutan, interval tidak sama | Skala Likert (1-5) | Median, Spearman |
| **Interval** | Jarak bermakna, tanpa nol absolut | Suhu Celsius | Mean, Pearson, t-test |
| **Ratio** | Jarak bermakna + nol absolut | Waktu eksekusi (ms), memory (bytes) | Semua operasi |

Tipe data menentukan uji statistik yang valid. Kebanyakan metrik performa TI = ratio; persepsi pengguna = ordinal.

### Kriteria Pemilihan Metrik

- **Representative** — Mewakili konsep yang diteliti
- **Sensitive** — Cukup peka menangkap perbedaan bermakna (hindari ceiling effect)
- **Feasible** — Bisa dikumpulkan dalam batasan waktu dan biaya

### Pre-registration

Metrik harus ditentukan **sebelum** eksperimen. Memilih metrik setelah melihat data = **p-hacking**. Metrik tambahan yang ditemukan kemudian dilaporkan sebagai *exploratory*, bukan *confirmatory*.

### Primary vs Secondary Metric

- **Primary Metric** — Langsung terikat ke hipotesis, menentukan kesimpulan
- **Secondary Metric** — Pendukung, dilaporkan di samping primary; statusnya suplementer

### Research vs Engineering

| Aspek | Engineering | Research |
|:------|:-----------|:----------|
| Pemilihan metrik | Berdasarkan kebiasaan/tool yang ada | Berdasarkan construct validity |
| Anomali | Dihapus untuk laporan bersih | Diinvestigasi — bisa jadi temuan |
| Kapan dipilih | Setelah sistem jadi (monitoring) | Sebelum eksperimen (by design) |

### Istilah Penting

- **Operationalization** — Transformasi konsep abstrak menjadi variabel terukur
- **Construct Validity** — Sejauh mana pengukuran benar-benar mengukur konsep yang dimaksud
- **Measurement Scale** — Klasifikasi data (NOIR) yang menentukan analisis valid
- **Multi-metric Evaluation** — Menggunakan beberapa metrik untuk menangkap konsep kompleks

---

# WS-05: Variabel & Metrik
**Mata Kuliah:** Riset Teknologi Informasi

---

## VARIABLE & METRIC DEFINITION

**Research Question:**  
Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara ArrayList<Person> dan HashMap<Integer, Person> pada 5 operasi CRUD dasar untuk 4 ukuran dataset (10³–10⁶) di Java 17 LTS?

---

### Tabel Definisi Variabel, Metrik & Justifikasi

| Variabel | Tipe | Konsep Abstrak | Metrik Konkret | Skala (NOIR) | Satuan | Cara Mengukur | Justifikasi |
|:---------|:----:|:---------------|:---------------|:------------:|:------:|:--------------|:------------|
| **Struktur data** | IV | Implementasi koleksi yang digunakan | Kategori: ArrayList<Person> vs HashMap<Integer, Person> | Nominal | — | Konfigurasi di config file: `data_structure: ["ArrayList", "HashMap"]` | Variabel independen yang dimanipulasi untuk membandingkan performa; nominal karena tidak ada urutan |
| **Jenis operasi** | IV | Operasi CRUD yang dijalankan | Kategori: insert, search, update, delete, iterate | Nominal | — | Konfigurasi di config file: `operations: ["insert", "search", "update", "delete", "iterate"]` | Variabel independen yang dimanipulasi; nominal karena tidak ada urutan operasi |
| **Ukuran dataset** | IV | Jumlah elemen dalam koleksi | Numerik: 10³, 10⁴, 10⁵, 10⁶ | Ratio | elemen | Konfigurasi di config file: `dataset_sizes: [1000, 10000, 100000, 1000000]` | Variabel independen yang dimanipulasi; ratio karena ada nol absolut (0 elemen) |
| **Execution time** | DV | Durasi eksekusi operasi | Rata-rata waktu per operasi | Ratio | ns/op | JMH mengukur dengan `@Benchmark`, output dalam ns/op dengan confidence interval 99% | **Primary metric** — langsung terikat H1a (HashMap lebih cepat di search); ratio karena ada nol absolut (0 ns) |
| **Memory footprint** | DV | Ukuran memori yang digunakan | Total memory instance + referenced objects | Ratio | bytes | JOL `GraphLayout.parseInstance().totalSize()` untuk shallow + deep size | **Primary metric** — langsung terikat H1c (ArrayList lebih hemat memori pada dataset kecil); ratio karena ada nol absolut (0 bytes) |
| **Throughput** | DV | Jumlah operasi per detik | Operasi yang berhasil per satuan waktu | Ratio | ops/sec | JMH output `ops/sec` (inverse dari ns/op) | **Secondary metric** — pendukung untuk melihat throughput praktis; ratio karena ada nol absolut |
| **Jumlah produk** | CV | Jumlah elemen dalam dataset | Dikunci pada 4 level: 10³, 10⁴, 10⁵, 10⁶ | Ratio | elemen | Dikunci di config file untuk semua eksperimen | Control variable untuk memastikan semua eksperimen menggunakan dataset yang sama |
| **JVM version** | CV | Versi Java Runtime Environment | Dikunci pada Java 17 LTS | Nominal | — | Dikunci di environment: `JAVA_HOME=/usr/lib/jvm/java-17-openjdk` | Control variable untuk memastikan fair comparison; nominal karena versi adalah kategori |
| **GC algorithm** | CV | Garbage collector yang digunakan | Dikunci pada G1GC | Nominal | — | Dikunci di JVM flag: `-XX:+UseG1GC` | Control variable untuk memastikan GC behavior konsisten; nominal karena GC adalah kategori |
| **Heap size** | CV | Ukuran heap memory | Dikunci pada 4GB | Ratio | GB | Dikunci di JVM flag: `-Xms4g -Xmx4g` | Control variable untuk memastikan memory pressure konsisten; ratio karena ada nol absolut |
| **Warmup iterations** | CV | Jumlah iterasi warmup sebelum measurement | Dikunci pada 5 × 1 detik | Ratio | iterasi | Dikunci di JMH annotation: `@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)` | Control variable untuk memastikan JIT compilation selesai sebelum measurement |
| **Measurement iterations** | CV | Jumlah iterasi measurement | Dikunci pada 10 × 1 detik | Ratio | iterasi | Dikunci di JMH annotation: `@Measurement(iterations = 10, time = 1, timeUnit = TimeUnit.SECONDS)` | Control variable untuk memastikan cukup data untuk statistical analysis |
| **Forks** | CV | Jumlah JVM instance terpisah | Dikunci pada 3 forks | Ratio | forks | Dikunci di JMH annotation: `@Fork(value = 3)` | Control variable untuk menangkap variabilitas JIT compilation antar JVM instance |

---

### Alignment Check

```
Problem → Concept → Variable → Metric → Data → Result
```

- [X] **Problem:** Developer memilih struktur data tanpa panduan empiris
- [X] **Concept:** Performa (kecepatan, efisiensi memori, throughput)
- [X] **Variable:** ArrayList vs HashMap, 5 operasi, 4 ukuran dataset
- [X] **Metric:** ns/op, bytes, ops/sec dengan confidence interval 99%
- [X] **Data:** JMH output CSV + JSON dengan raw measurements
- [X] **Result:** Decision matrix untuk developer

**Setiap langkah terdokumentasi:** ✓  
**Tidak ada lompatan logis:** ✓  
**Metrik mengukur apa yang dimaksud (construct validity):** ✓

---

# Latihan 1 — Operationalization Chain

**RQ:** Bagaimana perbedaan performa ArrayList vs HashMap pada 5 operasi CRUD untuk 4 ukuran dataset di Java 17?

| Variabel | Tipe | Konsep Abstrak | Metrik Konkret | Skala (NOIR) | Satuan |
|:---------|:----:|:---------------|:---------------|:------------:|:------:|
| Struktur data | IV | Implementasi koleksi | ArrayList vs HashMap | Nominal | — |
| Jenis operasi | IV | Operasi CRUD | insert, search, update, delete, iterate | Nominal | — |
| Ukuran dataset | IV | Jumlah elemen | 10³, 10⁴, 10⁵, 10⁶ | Ratio | elemen |
| Execution time | DV | Durasi eksekusi | ns/op dengan CI 99% | Ratio | ns/op |
| Memory footprint | DV | Ukuran memori | bytes via JOL | Ratio | bytes |
| Throughput | DV | Operasi per detik | ops/sec | Ratio | ops/sec |
| JVM version | CV | Java runtime | Java 17 LTS | Nominal | — |
| GC algorithm | CV | Garbage collector | G1GC | Nominal | — |
| Heap size | CV | Memory heap | 4GB fixed | Ratio | GB |

**Apakah ada lompatan logis dalam rantai?** [ ] Ya / [X] Tidak

> Jika ya, di mana? Rantai sudah lengkap dan logis. Setiap konsep abstrak diterjemahkan menjadi metrik konkret dengan skala dan satuan yang jelas.

---

# Latihan 2 — Evaluasi Metrik

**Evaluasi metrik DV yang dipilih menggunakan 3 kriteria:**

| Kriteria | Skor (1-5) | Justifikasi |
|:---------|:---------:|:------------|
| **Representative** | 5 | Execution time (ns/op) langsung mewakili kecepatan operasi; memory footprint (bytes) mewakili efisiensi memori; throughput (ops/sec) mewakili kapasitas operasi per detik. Ketiga metrik secara langsung menjawab RQ tentang perbedaan performa. |
| **Sensitive** | 5 | Ketiga metrik cukup peka menangkap perbedaan performa antar struktur data. Execution time sangat sensitif terhadap kompleksitas operasi (O(1) vs O(n)); memory sensitif terhadap overhead struktur data; throughput sensitif terhadap latency. Tidak ada ceiling effect karena range nilai sangat lebar (ns hingga ms untuk time, bytes hingga MB untuk memory). |
| **Feasible** | 5 | Semua metrik dapat dikumpulkan dari JMH (execution time, throughput) dan JOL (memory) tanpa biaya tambahan. JMH dan JOL adalah tools open-source yang sudah mature dan widely used dalam Java community. Tidak memerlukan hardware khusus atau setup kompleks. |

**Apakah perlu secondary metric?** [X] Ya / [ ] Tidak

> Jika ya, apa dan mengapa?
> 
> **Secondary metrics yang ditambahkan:**
> 1. **GC pause time** — Mengukur waktu pause akibat garbage collection. Penting karena HashMap bisa trigger GC lebih sering akibat memory overhead. Diukur via JMH GC profiler.
> 2. **Allocation rate** — Mengukur jumlah object allocation per operasi. Penting untuk memahami GC pressure. Diukur via JMH allocation profiler.
> 3. **Cache miss rate** — Mengukur cache misses (via perf tool di Linux). Penting untuk memahami memory access pattern, terutama untuk iterate operation.
> 
> Ketiga secondary metrics ini memberikan gambaran lebih lengkap tentang performa praktis dan trade-off antara ArrayList dan HashMap.

**Contoh kasus ceiling effect untuk metrik ini:**

> Ceiling effect bisa terjadi pada metrik throughput jika semua operasi mencapai throughput maksimal (misal 10⁹ ops/sec) pada dataset kecil. Dalam kasus ini, metrik tidak lagi sensitif membedakan performa antar struktur data pada dataset kecil. Untuk mengatasi ini, bisa ditambahkan metrik yang lebih granular seperti "latency percentile (p95, p99)" yang lebih peka terhadap perbedaan kecil dalam throughput.

---

# Latihan 3 — Data Quality Check

**Bayangkan data yang akan dikumpulkan dari eksperimen. Evaluasi 4 dimensi kualitas data:**

| Dimensi | Pertanyaan | Jawaban | Strategi Mitigasi |
|:--------|:-----------|:--------|:------------------|
| **Completeness** | Apakah semua data point terkumpul? | Semua kombinasi IV (2 struktur data × 5 operasi × 4 ukuran × 3 forks = 120 benchmark runs) akan terkumpul dari JMH otomatis. Tidak ada missing values karena JMH akan error jika ada yang gagal. | Menggunakan JMH yang robust; jika ada error, akan terdeteksi langsung dan eksperimen di-rerun. |
| **Consistency** | Apakah ada kontradiksi internal? | Potensi inkonsistensi minimal karena JMH menangani timing secara otomatis. Namun ada potensi inkonsistensi antara JMH timing (ns/op) dan JOL memory measurement (bytes) jika dijalankan pada waktu berbeda (GC bisa terjadi di antara). | Menjalankan JMH dan JOL dalam satu benchmark method untuk memastikan consistency; menggunakan seed yang sama untuk dataset generation. |
| **Validity** | Apakah benar-benar mengukur yang dimaksud? | Execution time valid mengukur kecepatan operasi (JMH adalah standar); memory valid jika menggunakan JOL yang terkalibrasi; throughput valid karena inverse dari execution time. Namun ada asumsi bahwa single-threaded measurement valid untuk production use case (production bisa multi-threaded). | Melakukan pre-test dengan data sampel; melakukan validation bahwa JMH output konsisten dengan manual timing; mendokumentasikan asumsi single-threaded. |
| **Representativeness** | Apakah sampel mewakili populasi target? | Data dari Java 17 LTS dengan G1GC mungkin tidak mewakili semua Java environment (ada Java 8, 11, 21, berbagai GC). Distribusi data uniform random mungkin tidak mencerminkan real-world data (skewed, clustered). | Melakukan sensitivity analysis dengan variasi Java version (jika memungkinkan); melakukan cross-validation dengan data real-world dari aplikasi production (jika bisa akses); mendokumentasikan batasan generalisasi dengan jelas. |

---

# Refleksi

**Pertanyaan:** Mengapa memilih metrik setelah melihat data dianggap p-hacking? Apa bedanya dengan eksplorasi data yang sah?

**Jawaban:**

**P-hacking** adalah praktik memilih metrik atau analisis statistik setelah melihat hasil data dengan tujuan untuk mendapatkan p-value < 0.05 agar hipotesis terlihat signifikan. Ini melanggar prinsip falsifiability karena peneliti secara implisit "menyesuaikan" pertanyaan dengan jawaban yang sudah ada.

**Perbedaan dengan eksplorasi data yang sah:**
- **P-hacking**: Metrik dipilih SETELAH melihat data dengan tujuan menemukan signifikansi (confirmatory bias)
- **Eksplorasi sah**: Metrik tambahan ditemukan SETELAH analisis utama selesai, dilaporkan sebagai "exploratory findings" (bukan confirmatory), dan dinyatakan dengan jelas bahwa ini adalah post-hoc analysis yang memerlukan validasi lebih lanjut

**Strategi untuk menghindari p-hacking:**

1. **Pre-registration** — Tentukan metrik dan analisis SEBELUM eksperimen dimulai. Publikasikan di platform seperti OSF (Open Science Framework) atau dalam protocol paper.

2. **Primary vs Secondary** — Pisahkan metrik utama (untuk menjawab hipotesis) dari metrik tambahan (untuk eksplorasi). Hanya primary metrics yang digunakan untuk kesimpulan utama.

3. **Transparansi** — Laporkan semua analisis yang dilakukan, bukan hanya yang signifikan. Jika ada 10 metrik yang diuji dan hanya 2 yang signifikan, laporkan semua 10 dengan p-value masing-masing.

4. **Bonferroni correction** — Jika melakukan multiple testing (misal 5 operasi × 4 ukuran = 20 pairwise comparisons), gunakan koreksi statistik untuk mengurangi false positive rate. Contoh: p-value threshold menjadi 0.05/20 = 0.0025 untuk setiap test.

5. **Effect size** — Laporkan effect size (Cohen's d, Hedges' g) selain p-value. Effect size lebih robust terhadap sample size dan lebih informatif tentang practical significance.

**Dalam konteks riset ini:**
- Primary metrics: execution time (ns/op), memory footprint (bytes) — pre-registered sebelum eksperimen
- Secondary metrics: GC pause time, allocation rate, cache miss rate — dilaporkan sebagai exploratory findings
- Semua 120 benchmark runs akan dilaporkan (tidak cherry-pick)
- Bonferroni correction akan diterapkan untuk 20 pairwise comparisons (5 operasi × 4 ukuran)
- Effect size (Cohen's d) akan dilaporkan untuk setiap comparison