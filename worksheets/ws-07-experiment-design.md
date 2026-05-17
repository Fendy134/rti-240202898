# WS-07: Experimental Design & Validity

> **Bab 7 — Experimental Design & Validity**

---

## Ringkasan Materi

### Correlation ≠ Causality

Kausalitas membutuhkan 3 syarat:
1. **Covariance** — X dan Y bergerak bersama
2. **Temporal precedence** — X berubah sebelum Y
3. **Elimination of alternatives** — Tidak ada faktor lain yang menjelaskan Y

Controlled experiment adalah satu-satunya metode yang bisa membuktikan kausalitas.

### Empat Jenis Validitas

| Jenis | Pertanyaan | Ancaman Umum |
|-------|-----------|-------------|
| **Internal** | Apakah hubungan IV→DV nyata? | Confounding variable (GC, JIT), selection bias |
| **External** | Apakah bisa digeneralisasi? | Dataset terlalu spesifik (uniform random saja) |
| **Construct** | Apakah mengukur konsep yang benar? | Metrik tidak sesuai (ns/op vs real-world latency) |
| **Conclusion** | Apakah kesimpulan statistik valid? | Sample size kecil, uji salah, p-hacking |

Internal dan external validity sering berkonflik: semakin terkontrol (internal kuat) → semakin artificial (external lemah).

### Tiga Tipe Eksperimen dalam Riset TI

| Tipe | Deskripsi | Kapan Digunakan |
|------|----------|----------------|
| **Comparison Study** | Metode A vs B pada kondisi identik | Membandingkan ArrayList vs HashMap pada operasi sama |
| **Ablation Study** | Full system → lepas komponen satu per satu | Mengukur kontribusi JIT warmup, GC, dataset size |
| **Parameter Study** | Variasikan satu parameter, amati dampak | Uji sensitifitas terhadap heap size, GC algorithm |

### Fairness dalam Perbandingan

Perbandingan yang adil = **kondisi identik** untuk semua metode: dataset sama, preprocessing sama, tuning effort sebanding, environment sama, metrik sama.

Contoh tidak adil: HashMap dengan tuning hash function vs ArrayList default → hasilnya misleading.

### Threats to Validity = Diidentifikasi Sebelum Eksperimen

Ancaman validitas harus diidentifikasi **sebelum** eksperimen dan mitigasinya dirancang sebagai bagian dari desain — bukan ditulis sebagai boilerplate setelah selesai.

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan testing | Memastikan sistem memenuhi requirement | Membuktikan hubungan kausal antar variabel |
| Baseline | Versi sebelumnya (last release) | Metode tervalidasi dari literatur (Gorelick & Ozsvald 2020) |
| Kegagalan | Bug → fix → release | H₀ tidak ditolak → tetap kontribusi ilmiah |
| Sukses | 100% test pass | Evidence valid — mendukung atau menolak hipotesis |

### Istilah Penting

- **Causality** — Hubungan sebab-akibat (covariance + temporal + elimination)
- **Controlled Experiment** — Ubah satu variabel (struktur data), kontrol sisanya (dataset, JVM), amati efek (execution time)
- **Fairness** — Semua struktur data diuji pada kondisi yang benar-benar identik
- **Threats to Validity** — Faktor yang bisa melemahkan kesimpulan jika tidak dimitigasi
- **Conclusion Validity** — Validitas statistik: power, sample size, uji yang tepat

---

# WS-07: Experimental Design & Validity
**Mata Kuliah:** Riset Teknologi Informasi

---

## EXPERIMENT DESIGN

**Research Question:**  
Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara ArrayList<Person> dan HashMap<Integer, Person> pada 5 operasi CRUD dasar untuk 4 ukuran dataset (10³–10⁶) di Java 17 LTS?

**Hypothesis:**  
H₀: Tidak ada perbedaan signifikan dalam performa antara ArrayList dan HashMap (p > 0.05)  
H₁: Ada perbedaan signifikan, dengan pola: HashMap lebih cepat di search (O(1) vs O(n)), ArrayList lebih cepat di iterate (cache locality), ArrayList lebih hemat memori pada dataset kecil

**Tipe Eksperimen:** [X] Comparison Study / [ ] Ablation Study / [ ] Parameter Study

---

### Kondisi Eksperimen

| Kondisi | Deskripsi | IV Value | CV Settings |
|---------|-----------|----------|-------------|
| **Condition 1** | ArrayList pada 5 operasi CRUD | ArrayList<Person> | Java 17, G1GC, 4GB heap, seed=42, 10³–10⁶ elemen |
| **Condition 2** | HashMap pada 5 operasi CRUD | HashMap<Integer, Person> | Java 17, G1GC, 4GB heap, seed=42, 10³–10⁶ elemen |

**Fairness Checklist:**
- [X] **Dataset identik** — Sama-sama menggunakan POJO Person (id, name, age, email) dengan seed=42 untuk reproducibility
- [X] **Preprocessing setara** — Kedua struktur data di-populate dengan cara yang sama: loop insert 1 juta kali
- [X] **Tuning effort setara** — Tidak ada custom hash function atau optimization khusus untuk HashMap; ArrayList juga tidak di-optimize
- [X] **Environment identik** — Sama-sama Java 17 LTS, G1GC, 4GB heap fixed, single-threaded, 5 warmup × 1s, 10 measurement × 1s, 3 forks
- [X] **Metrik evaluasi sama** — Kedua struktur data diukur dengan metrik yang sama: ns/op (JMH), bytes (JOL), ops/sec

---

### Threat Analysis

| Threat Type | Ancaman Spesifik | Mitigasi | Status |
|-------------|-----------------|----------|--------|
| **Internal Validity** | JIT compilation non-deterministic — hasil bisa berbeda antar run | Menggunakan JMH dengan 5 warmup iterations untuk memastikan JIT selesai sebelum measurement; menjalankan 3 forks untuk menangkap variabilitas | ✅ Dimitigasi |
| **Internal Validity** | GC pause bisa terjadi di tengah measurement — mempengaruhi execution time | Menggunakan JMH GC profiler untuk mendeteksi GC pause; melaporkan hasil dengan dan tanpa GC pause; menggunakan heap 4GB fixed untuk meminimalkan GC frequency | ✅ Dimitigasi |
| **Internal Validity** | OS scheduler bisa context-switch — mempengaruhi timing | Menjalankan eksperimen pada mesin yang idle; menutup aplikasi background; menggunakan CPU affinity jika memungkinkan | ⚠️ Partial |
| **Internal Validity** | Hash collision di HashMap — bisa mempengaruhi performa search | Menggunakan seed tetap (seed=42) untuk reproducibility; melaporkan hash collision rate; jika ada anomali, investigasi penyebabnya | ✅ Dimitigasi |
| **External Validity** | Dataset uniform random — tidak mencerminkan real-world data distribution | Melaporkan batasan: hasil hanya valid untuk uniform random distribution; menyarankan future work untuk test dengan skewed/clustered distribution | ⚠️ Acknowledged |
| **External Validity** | Single-threaded — tidak mencerminkan concurrent access di production | Melaporkan batasan: hasil hanya valid untuk single-threaded scenario; menyarankan future work untuk test dengan ConcurrentHashMap dan multi-threaded access | ⚠️ Acknowledged |
| **External Validity** | POJO sederhana (4 fields) — tidak mencerminkan complex object graphs | Melaporkan batasan: hasil hanya valid untuk POJO sederhana; menyarankan future work untuk test dengan nested objects | ⚠️ Acknowledged |
| **Construct Validity** | ns/op tidak mencerminkan real-world latency (ada GC, context-switch, cache miss) | Menggunakan JMH yang menangani GC/JIT; melaporkan secondary metrics (GC pause, allocation rate, cache miss); menggunakan confidence interval 99% untuk menangkap variabilitas | ✅ Dimitigasi |
| **Construct Validity** | Memory footprint (bytes) tidak mencerminkan actual heap pressure | Menggunakan JOL untuk precise measurement (shallow + deep size); melaporkan allocation rate sebagai secondary metric | ✅ Dimitigasi |
| **Conclusion Validity** | Multiple comparisons (5 operasi × 4 ukuran = 20 pairwise) → false positive rate tinggi | Menggunakan Bonferroni correction: p-value threshold = 0.05/20 = 0.0025 untuk setiap test; melaporkan effect size (Cohen's d) selain p-value | ✅ Dimitigasi |
| **Conclusion Validity** | Sample size kecil (3 forks × 10 iterations = 30 samples per condition) | Menggunakan power analysis untuk memastikan sample size cukup; jika power < 0.8, menambah iterations atau forks | ✅ Dimitigasi |
| **Conclusion Validity** | Uji statistik salah (parametric vs non-parametric) | Melakukan normality test (Shapiro-Wilk) terlebih dahulu; jika data normal, gunakan ANOVA; jika tidak, gunakan Kruskal-Wallis | ✅ Dimitigasi |

---

### Statistical Plan

**Uji Statistik Utama:**  
Two-way ANOVA dengan faktor: struktur data (ArrayList vs HashMap) × operasi (insert, search, update, delete, iterate) × ukuran dataset (10³, 10⁴, 10⁵, 10⁶)

**Justifikasi:**  
Two-way ANOVA memungkinkan kita menganalisis efek utama (struktur data, operasi, ukuran) dan interaksi antar faktor (misal: apakah perbedaan ArrayList vs HashMap bergantung pada operasi atau ukuran dataset).

**Alpha (Significance Level):**  
0.05 (standard), dengan Bonferroni correction untuk multiple comparisons: 0.05/20 = 0.0025

**Effect Size Minimum (Practical Significance):**  
Cohen's d > 0.5 (medium effect size) — perbedaan >50% dianggap praktis signifikan untuk decision making

**Post-hoc Test:**  
Tukey HSD (Honestly Significant Difference) untuk pairwise comparison antar struktur data pada setiap kombinasi operasi × ukuran

**Power Analysis:**  
Target power = 0.8 (80% chance mendeteksi efek jika ada). Jika power < 0.8, tambah iterations atau forks.

**Confidence Interval:**  
99% untuk semua measurement (lebih ketat dari standard 95% karena JIT/GC variabilitas tinggi)

---

# Latihan 1 — Desain Eksperimen

**RQ:** Bagaimana perbedaan performa ArrayList vs HashMap pada 5 operasi CRUD untuk 4 ukuran dataset di Java 17?

**Tipe eksperimen:** [X] Comparison / [ ] Ablation / [ ] Parameter

| Kondisi | Deskripsi | IV Value | CV Settings |
|---------|-----------|----------|-------------|
| **Condition 1** | ArrayList pada 5 operasi CRUD | ArrayList<Person> | Java 17, G1GC, 4GB heap, seed=42, 10³–10⁶ elemen, 5 warmup, 10 measurement, 3 forks |
| **Condition 2** | HashMap pada 5 operasi CRUD | HashMap<Integer, Person> | Java 17, G1GC, 4GB heap, seed=42, 10³–10⁶ elemen, 5 warmup, 10 measurement, 3 forks |

---

# Latihan 2 — Fairness Checklist

**Evaluasi apakah desain eksperimen sudah fair:**

| Kriteria | Status | Detail |
|----------|--------|--------|
| **Dataset identik** | ✅ | Sama-sama POJO Person (id, name, age, email), seed=42, 10³–10⁶ elemen |
| **Preprocessing setara** | ✅ | Kedua struktur data di-populate dengan loop insert yang sama, tanpa optimization khusus |
| **Tuning effort setara** | ✅ | Tidak ada custom hash function untuk HashMap, tidak ada optimization untuk ArrayList |
| **Environment identik** | ✅ | Java 17 LTS, G1GC, 4GB heap fixed, single-threaded, 5 warmup × 1s, 10 measurement × 1s, 3 forks |
| **Metrik evaluasi sama** | ✅ | Kedua struktur data diukur dengan ns/op (JMH), bytes (JOL), ops/sec |

**Ada yang tidak fair?** [ ] Ya / [X] Tidak

> Jika ya, bagaimana cara memperbaikinya? Semua kriteria fairness sudah terpenuhi. Desain eksperimen sudah fair untuk perbandingan ArrayList vs HashMap.

---

# Latihan 3 — Threat Analysis

**Identifikasi ancaman validitas untuk desain eksperimen ini:**

| Threat Type | Ancaman Spesifik | Mitigasi |
|-------------|-----------------|----------|
| **Internal** | JIT compilation non-deterministic | 5 warmup iterations, 3 forks untuk menangkap variabilitas |
| **Internal** | GC pause di tengah measurement | JMH GC profiler, heap 4GB fixed, lapor dengan/tanpa GC pause |
| **Internal** | OS scheduler context-switch | Jalankan pada mesin idle, tutup background apps, CPU affinity |
| **Internal** | Hash collision di HashMap | Seed tetap (42), lapor collision rate, investigasi anomali |
| **External** | Dataset uniform random saja | Lapor batasan, saran future work dengan skewed/clustered data |
| **External** | Single-threaded saja | Lapor batasan, saran future work dengan ConcurrentHashMap |
| **External** | POJO sederhana saja | Lapor batasan, saran future work dengan nested objects |
| **Construct** | ns/op tidak mencerminkan real latency | JMH handles GC/JIT, secondary metrics (GC pause, allocation), CI 99% |
| **Construct** | Memory bytes tidak mencerminkan heap pressure | JOL precise measurement, allocation rate secondary metric |
| **Conclusion** | Multiple comparisons false positive | Bonferroni correction (0.05/20 = 0.0025), effect size Cohen's d |
| **Conclusion** | Sample size kecil | Power analysis, target power 0.8, tambah iterations jika perlu |
| **Conclusion** | Uji statistik salah | Normality test (Shapiro-Wilk), ANOVA atau Kruskal-Wallis sesuai distribusi |

**Ancaman mana yang paling sulit dimitigasi?** **External Validity — Dataset uniform random saja**

**Mengapa?**
> Karena untuk mengevaluasi dengan real-world data distribution (skewed, clustered, dengan duplicates), memerlukan akses ke production data yang sering confidential atau tidak tersedia. Selain itu, real-world data bisa sangat bervariasi antar aplikasi, sehingga sulit untuk membuat dataset "representative" yang universal. Mitigasi terbaik adalah melaporkan batasan dengan jelas dan menyarankan future work untuk test dengan berbagai distribusi data.

---

# Refleksi

**Pertanyaan:** Sebuah paper melaporkan "HashMap mengalahkan ArrayList di semua operasi." Apa 3 pertanyaan pertama yang harus diajukan untuk mengevaluasi klaim ini?

**Jawaban:**

1. **"Apakah perbandingan dilakukan pada kondisi yang benar-benar identik?"**  
   Pertanyaan ini mengevaluasi **fairness**. Apakah dataset sama? Preprocessing sama? Tuning effort sama? Environment sama? Jika ada perbedaan kondisi, klaim "HashMap mengalahkan ArrayList" bisa misleading. Contoh: jika HashMap di-tune dengan custom hash function tapi ArrayList tidak, perbandingan tidak fair.

2. **"Apakah perbedaan signifikan secara statistik dan praktis?"**  
   Pertanyaan ini mengevaluasi **conclusion validity**. Apakah p-value < 0.05? Apakah effect size (Cohen's d) > 0.5? Jika p-value > 0.05 atau effect size kecil, klaim "mengalahkan" terlalu kuat. Contoh: HashMap 1% lebih cepat tapi p-value = 0.1 → tidak signifikan.

3. **"Apakah hasil bisa digeneralisasi ke konteks lain?"**  
   Pertanyaan ini mengevaluasi **external validity**. Apakah dataset representative? Apakah single-threaded atau multi-threaded? Apakah POJO sederhana atau complex object? Jika hanya test pada uniform random single-threaded POJO sederhana, klaim "HashMap mengalahkan ArrayList" hanya berlaku untuk konteks itu, tidak universal.

**Bonus pertanyaan:**

4. **"Apakah ada ancaman validitas yang tidak dimitigasi?"**  
   Contoh: GC pause tidak dikontrol, JIT warmup tidak cukup, multiple comparisons tanpa correction → kesimpulan bisa salah.

5. **"Apakah hasil konsisten dengan teori?"**  
   Contoh: HashMap O(1) lookup vs ArrayList O(n) search → expected HashMap lebih cepat di search. Jika hasil sebaliknya, ada yang salah (measurement error, implementation bug, atau teori tidak berlaku di konteks ini).