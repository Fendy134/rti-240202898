@# WS-09: Implementation & Environment

> **Bab 9 — Implementasi Riset & Kontrol Lingkungan**

---

## Ringkasan Materi

### Implementasi Riset ≠ Coding Biasa

Tujuan implementasi riset bukan membuat software yang berfungsi, melainkan membangun **instrumen pengukuran yang konsisten**. Setiap modul harus di-mapping ke variabel (dari Bab 6), parameter harus config-driven, dan logging aktif dari hari pertama.

### Reproducible Implementation Model

```
Design → Implementation → Environment Setup → Execution Consistency → Reproducibility → Trustworthy Result
```

Setiap transisi memiliki syarat:
- Design → Implementation: kode sesuai mapping variabel-ke-komponen
- Implementation → Environment: versi, dependency, seed, path, OS eksplisit
- Environment → Consistency: seed terkunci, urutan deterministik
- Consistency → Reproducibility: dokumentasi lengkap
- Reproducibility → Trust: siapa pun ikuti dokumentasi → hasil sama/serupa

### Repeatability vs Reproducibility

| Level | Peneliti | Environment | Hasil |
|-------|---------|-------------|-------|
| **Repeatability** | Sama | Sama | Sama persis |
| **Reproducibility** | Berbeda | Berbeda (ikuti docs) | Sama/serupa |

Capai **repeatability** dulu, baru **reproducibility**.

### Engineering vs Research Perspective

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Tujuan | Sistem berfungsi untuk user | Instrumen pengukuran konsisten |
| Dependency | Update ke terbaru | Lock di versi spesifik |
| Testing | Unit, integration, E2E | Repeatability test (run ulang → sama?) |
| Dokumentasi | User guide, API docs | Environment spec, execution steps, expected output |
| Config | Default masuk akal | Setiap parameter eksplisit & adjustable |

### Jebakan Kognitif

1. Menunda environment setup → bug sulit dilacak
2. Tidak pakai version control → hasil tidak bisa direkonstruksi
3. Menolak Docker/container → "di laptop saya bisa" saat review
4. 3× hasil sama ≠ repeatable (bisa cache/state tersimpan)

### Istilah Penting

- **Environment Specification** — Deskripsi lengkap: hardware, OS, runtime, library + versi, config, seed
- **Dependency** — Komponen eksternal yang harus di-lock versinya
- **Config-driven** — Parameter dieksternalisasi ke file konfigurasi, bukan hardcode

---

## Template A.9 — Dokumentasi Setup Eksperimen

```
EXPERIMENT SETUP DOCUMENTATION

Hardware:
  CPU     : Intel Core i3 
  RAM     : 16 GB DDR4
  GPU     : N/A (CPU Benchmark Only)
  Storage : SSD (SATA/NVMe)

Software:
  OS        : Windows (11)
  Runtime   : OpenJDK 17 LTS (Java 17.0.19) / Python 3.13.13
  Framework : JMH (Java Microbenchmark Harness) 1.37

Dependencies:
| Library | Version | Sumber | Hash/Checksum |
|---------|---------|--------|---------------|
| jmh-core| 1.37    | Maven Central | - |
| jmh-generator-annprocess | 1.37 | Maven Central | - |
| jol-core| 0.17    | Maven Central | - |
| pandas  | >=2.0.0 | PyPI   | - |
| scipy   | >=1.11.0| PyPI   | - |
| statsmodels | >=0.14.0 | PyPI | - |

Konfigurasi:
  Config file     : pom.xml / requirements.txt / run_benchmark.sh
  Random seed     : 42 (DatasetGenerator.java)
  Hyperparameters : Warmup=5, Measurement=10, Forks=3, Heap=4G

Reproducibility Check:
  [x] Dependency terdokumentasi (requirements.txt / lock file)
  [x] Seed ditetapkan di semua level (Python, NumPy, framework)
  [x] Config di version control
  [x] README instruksi reproduksi lengkap
```

---

## Latihan 1 — Environment Specification

Dokumentasikan environment untuk eksperimen Anda 
| Komponen | Spesifikasi |
|----------|------------|
| CPU | Intel Core i7  |
| RAM | 16 GB DDR4 |
| GPU | CPU-only (tidak menggunakan GPU untuk benchmark) |
| OS | Windows 11 Pro |
| Runtime | OpenJDK 17 LTS (Java 17.0.x) |
| Framework | JMH 1.37 (Java Microbenchmark Harness) |
| Random Seed | 42 (untuk DatasetGenerator) |

**Dependencies (minimal 5):**

| Library | Version | Alasan Dibutuhkan |
|---------|---------|-------------------|
| JMH Core | 1.37 | Framework benchmark utama untuk timing measurement |
| JMH Annotation Processor | 1.37 | Generate boilerplate code untuk benchmark |
| JOL (Java Object Layout) | 0.17 | Memory footprint measurement (shallow + deep size) |
| Maven | 3.9.16 | Build tool untuk compile dan package JAR |
| Python | 3.13.13 | Statistical analysis (ANOVA, effect size, visualisasi) |
| pandas | 2.3.3 | Parse CSV hasil JMH dan data manipulation |
| numpy | 2.3.4 | Numerical computation untuk effect size |
| scipy | 1.17.1 | Statistical tests (Shapiro-Wilk, Levene) |
| statsmodels | latest | ANOVA dan post-hoc test |
| matplotlib + seaborn | latest | Visualisasi hasil benchmark |

---

## Latihan 2 — Repeatability Test Plan

Rancang tes repeatability sederhana: jalankan kode yang sama 3× di environment yang sama.

| Run | Seed | Metrik Utama | Hasil Sama? |
|-----|------|-------------|-------------|
| 1 | 42 | ArrayList.search @ 10⁶: 7,075,019 ns/op ± 1,633,238 | — |
| 2 | 42 | ArrayList.search @ 10⁶: dalam CI 99.9% dari Run 1 | [X] Ya |
| 3 | 42 | ArrayList.search @ 10⁶: dalam CI 99.9% dari Run 1 | [X] Ya |

**Jika hasil berbeda, kemungkinan penyebab:**
> JMH sudah menangani variabilitas dengan:
> - 5 warmup iterations untuk stabilkan JIT compilation
> - 10 measurement iterations untuk capture variability
> - 3 forks (JVM instances terpisah) untuk isolasi
> - Confidence interval 99.9% untuk quantify uncertainty
> 
> Hasil antar-run bisa berbeda dalam margin CI, tapi mean harus konsisten.

**Checklist kontrol yang sudah diterapkan:**
- [X] Random seed di-set di semua level (DatasetGenerator seed=42)
- [X] Tidak ada background process yang mengganggu (tutup Chrome, IDE idle)
- [X] Cache dibersihkan antar-run (JMH fork baru = JVM baru)
- [X] Config file yang sama untuk semua run (JVM flags: -Xms4g -Xmx4g -XX:+UseG1GC)
- [X] JMH GC profiler aktif untuk detect GC pause
- [X] Heap size fixed (4GB) untuk konsistensi memory behavior

---

## Latihan 3 — README Eksperimen

Tulis README minimum untuk eksperimen Anda (6 komponen wajib).

```markdown
# Judul Eksperimen: ArrayList vs HashMap Performance Benchmark (Java 17 LTS)

## 1. Environment

**Hardware:**
- CPU: Intel Core i3
- RAM: 16 GB DDR4
- Storage: SSD (untuk fast I/O)

**Software:**
- OS: Windows 11 Pro
- Java: OpenJDK 17 LTS
- Maven: 3.9.16
- Python: 3.13.13 (untuk analisis statistik)

**Dependencies:**
- JMH 1.37, JOL 0.17
- pandas 2.3.3, numpy 2.3.4, scipy 1.17.1

## 2. Installation

**Build benchmark JAR:**
```bash
cd benchmark-project
mvn clean package
```
Output: `target/benchmarks.jar` (2.92 MB)

**Install Python dependencies:**
```bash
cd analysis
pip install pandas numpy scipy statsmodels matplotlib seaborn
```

## 3. Data

**Sumber:** Synthetic data generated by `DatasetGenerator.java`

**Format:** POJO `Person` (id, name, age, email)

**Ukuran:** 10³, 10⁴, 10⁵, 10⁶ elements

**Seed:** 42 (deterministik, reproducible)

## 4. Execution

**Run full benchmark (~60 menit):**
```bash
java -jar target/benchmarks.jar -rf csv -rff results/results.csv
```

**Run statistical analysis:**
```bash
cd analysis
python analyze_final.py
```

## 5. Configuration

**JVM Flags:**
- `-Xms4g -Xmx4g` (heap 4GB fixed)
- `-XX:+UseG1GC` (G1 Garbage Collector)
- `-XX:+AlwaysPreTouch` (pre-allocate memory)

**JMH Parameters:**
- Warmup: 5 iterations × 1s
- Measurement: 10 iterations × 1s
- Forks: 3
- Mode: AverageTime + Throughput

## 6. Expected Output

**results.csv (80 rows):**
```csv
"Benchmark","Mode","Threads","Samples","Score","Score Error (99.9%)","Unit"
"ArrayListBenchmark.search","avgt",1,30,1128.62,135.86,"ns/op",1000
"HashMapBenchmark.search","avgt",1,30,14.44,0.85,"ns/op",1000
```

**Key Findings:**
- HashMap 94,014x faster di search @ 10⁶
- ArrayList 4.6x faster di iterate @ 10³
```

---

## Refleksi

> Apakah eksperimen Anda saat ini bisa direproduksi oleh orang lain tanpa bantuan Anda? Komponen apa yang masih hilang?

**Level saat ini:** [X] Repeatability / [X] Reproducibility (partial)

**Komponen yang sudah terdokumentasi:**
-  Environment specification lengkap
-  Build instructions (Maven)
-  Execution command dengan flags
-  Configuration eksplisit (JVM, JMH, seed)
-  Expected output dengan contoh
-  Source code di GitHub (siap push)
-  README dengan 6 komponen wajib

**Komponen yang bisa ditingkatkan:**
-  Docker container untuk full isolation
-  CI/CD pipeline (GitHub Actions)
-  Exact CPU model (tergantung mesin)
-  Maven lock file untuk checksum

**Kesimpulan:**
Eksperimen **reproducible** dengan dokumentasi yang ada. Siapa pun dengan Java 17 + Maven bisa clone repo, build, dan run dengan hasil konsisten dalam CI 99.9%.