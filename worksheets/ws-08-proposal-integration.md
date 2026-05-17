# WS-08: Proposal Integration (UTS)

> **Bab 8 — Proposal & Checkpoint**

---

## Ringkasan Materi

### Proposal = Satu Argumen Utuh

Proposal riset bukan kumpulan bab yang independen. Ia adalah **satu argumen** yang mengalir dari masalah ke rencana solusi. Jika satu koneksi putus, seluruh proposal kehilangan koherensi.

### Integration Map — 6 Koneksi Kritis

```
Problem (Bab 2) → Gap (Bab 3) → RQ & H (Bab 4) → Metrik (Bab 5) → Sistem (Bab 6) → Eksperimen (Bab 7)
```

| Koneksi | Pertanyaan Verifikasi |
|---------|----------------------|
| Problem → Gap | Apakah gap muncul dari analisis literatur terhadap masalah? |
| Gap → RQ | Apakah RQ langsung menjawab gap yang teridentifikasi? |
| RQ → Metrik | Apakah setiap variabel di RQ punya metrik terdefinisi? |
| Metrik → Sistem | Apakah setiap metrik bisa diukur oleh komponen sistem? |
| Sistem → Eksperimen | Apakah desain eksperimen menggunakan sistem sebagai instrumen? |

### Koherensi Vertikal + Horizontal

- **Vertikal** — Alur logis atas-ke-bawah (problem → experiment)
- **Horizontal** — Konsistensi terminologi (nama variabel di RQ = di hipotesis = di metrik = di desain)

### Jebakan Kognitif

| Jebakan | Deskripsi |
|---------|----------|
| "Selling" Introduction | Menulis promosi, bukan menyajikan data dan gap |
| Copy-paste Methodology | Menyalin deskripsi textbook tanpa menyesuaikan ke RQ |
| Optimistic Timeline | Meremehkan waktu implementasi; selalu tambah buffer 30-50% |
| No Possibility of Failure | Mengimplikasikan hasil pasti sukses — proposal jujur mengakui H₀ mungkin tidak ditolak |

### Struktur Proposal

1. **Pendahuluan** — Latar belakang + problem statement (Bab 1-2)
2. **Tinjauan Pustaka** — Literature review + gap + baseline (Bab 3)
3. **RQ / Kontribusi / Hipotesis** — (Bab 4)
4. **Metodologi** — Metrik + sistem + desain eksperimen (Bab 5-7)
5. **Timeline & Output**

### Istilah Penting

- **Integration Map** — Diagram 6 koneksi kritis antar komponen proposal
- **Vertical Coherence** — Alur logis atas-ke-bawah
- **Horizontal Coherence** — Konsistensi terminologi di semua bagian
- **Checkpoint** — Titik self-assessment sebelum transisi dari desain ke eksekusi

---

# WS-08: Proposal Integration (UTS)
**Mata Kuliah:** Riset Teknologi Informasi

---

## PROPOSAL LENGKAP

### Judul Proposal
**Analisis Perbandingan Performa Penggunaan ArrayList vs HashMap dalam Manajemen Data Objek pada Bahasa Pemrograman Java**

---

## Latihan 1 — Kompilasi Proposal Mini

Kumpulkan hasil dari WS-02 sampai WS-07 menjadi satu ringkasan proposal:

| Komponen | Sumber | Isi (1-2 kalimat) |
|----------|--------|-------------------|
| **Problem Statement** | WS-02 | Developer Java sering memilih struktur data koleksi berdasarkan intuisi tanpa panduan empiris yang valid. Pemilihan yang salah dapat menyebabkan performance bottleneck signifikan pada aplikasi production, terutama pada operasi data lookup dengan frekuensi tinggi. |
| **Gap** | WS-03 | Belum ada studi yang membandingkan ArrayList vs HashMap menggunakan JMH pada Java 17 LTS dengan statistical significance testing dan multi-size dataset (10³–10⁶). Studi existing menggunakan metodologi lemah (`System.currentTimeMillis()` single-run) sehingga hasil tidak reproducible dan tidak reliable untuk decision making. |
| **Research Question** | WS-04 | Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara ArrayList<Person> dan HashMap<Integer, Person> pada 5 operasi CRUD dasar (insert, search, update, delete, iterate) untuk 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶) di Java 17 LTS, diukur dengan JMH dan diuji signifikansinya secara statistik? |
| **Hipotesis** | WS-04 | H₀: Tidak ada perbedaan signifikan dalam performa antara ArrayList dan HashMap (p > 0.05). H₁: Ada perbedaan signifikan dengan pola: HashMap lebih cepat di search (O(1) vs O(n)), ArrayList lebih cepat di iterate (cache locality), ArrayList lebih hemat memori pada dataset kecil. |
| **Variabel & Metrik** | WS-05 | IV: struktur data (ArrayList vs HashMap), operasi (5 CRUD), ukuran dataset (10³–10⁶). DV: execution time (ns/op), memory footprint (bytes), throughput (ops/sec). CV: Java 17 LTS, G1GC, 4GB heap, 5 warmup, 10 measurement, 3 forks. |
| **Sistem** | WS-06 | JMH benchmark harness + JOL memory profiler dengan arsitektur modular dan config-driven execution. Setiap komponen (ArrayList/HashMap modul, 5 benchmark methods, data generator, measurement modules) dapat ditelusuri ke variabel riset. |
| **Desain Eksperimen** | WS-07 | Comparison study dengan 2 kondisi (ArrayList vs HashMap) pada kondisi identik (dataset sama, preprocessing sama, environment sama). Threat analysis mengidentifikasi 12 ancaman validitas dengan mitigasi spesifik. Statistical plan: Two-way ANOVA + Tukey HSD + Bonferroni correction (0.05/20 = 0.0025). |

---

## Latihan 2 — Integration Checklist

Verifikasi 6 koneksi kritis dengan merujuk tabel di Latihan 1:

| Koneksi | Status | Bukti |
|---------|--------|-------|
| **Problem → Gap** | ✅ | Gap muncul dari analisis 5 paper di WS-03 yang menunjukkan: (1) Pujiono et al. 2024 menggunakan `System.currentTimeMillis()` single-run tanpa warmup, (2) Gorelick & Ozsvald 2020 menggunakan JMH tapi tidak fokus ArrayList vs HashMap, (3) tidak ada paper yang menggunakan JMH + ArrayList vs HashMap + Java 17 LTS. |
| **Gap → RQ** | ✅ | RQ langsung menjawab gap: "Bagaimana perbedaan performa ArrayList vs HashMap pada Java 17 LTS diukur dengan JMH?" RQ spesifik pada 5 operasi CRUD, 4 ukuran dataset, dengan statistical testing. |
| **RQ → Hypothesis** | ✅ | H₁ memprediksi jawaban spesifik: HashMap lebih cepat di search (O(1) vs O(n)), ArrayList lebih cepat di iterate (cache locality), ArrayList lebih hemat memori pada dataset kecil. Threshold: p < 0.05, Cohen's d > 0.5. |
| **Hypothesis → Metric** | ✅ | Setiap variabel di H₁ punya metrik terukur: "lebih cepat" → execution time (ns/op), "lebih hemat memori" → memory footprint (bytes), "signifikan" → p-value < 0.05 + Cohen's d > 0.5. |
| **Metric → System** | ✅ | Setiap metrik bisa diukur oleh komponen sistem: execution time diukur JMH, memory diukur JOL, throughput dihitung dari execution time. Semua output terstruktur (CSV, JSON) untuk analisis. |
| **System → Experiment** | ✅ | Desain eksperimen menggunakan sistem sebagai instrumen: 2 kondisi (ArrayList vs HashMap) dijalankan melalui JMH dengan CV dikontrol (Java 17, G1GC, 4GB heap, 5 warmup, 10 measurement, 3 forks). Threat analysis mengidentifikasi 12 ancaman dengan mitigasi spesifik. |

**Koneksi mana yang paling lemah?** Semua koneksi sudah kuat dan terdokumentasi dengan baik.

**Bagaimana cara memperkuatnya?** Koneksi sudah cukup kuat. Jika perlu penguatan lebih lanjut, bisa menambahkan: (1) diagram visual integration map, (2) tabel cross-reference antara RQ ↔ Hypothesis ↔ Metric ↔ System ↔ Experiment, (3) pre-registration di OSF (Open Science Framework) untuk transparansi.

**Konsistensi horizontal — apakah istilah dan scope konsisten?** [X] Ya / [ ] Tidak

> Jika tidak, di bagian mana terjadi inkonsistensi?
> 
> **Verifikasi konsistensi:**
> - Istilah "ArrayList" dan "HashMap" konsisten di semua bagian (WS-02 sampai WS-07)
> - Istilah "5 operasi CRUD" (insert, search, update, delete, iterate) konsisten
> - Istilah "4 ukuran dataset" (10³, 10⁴, 10⁵, 10⁶) konsisten
> - Istilah "Java 17 LTS" konsisten
> - Istilah "execution time (ns/op)" konsisten
> - Istilah "memory footprint (bytes)" konsisten
> - Scope: single-threaded, uniform random distribution, POJO sederhana — konsisten di semua bagian

---

## Latihan 3 — Rubrik Self-Assessment

Evaluasi proposal mini menggunakan rubrik:

| Kriteria | Skor (1-3) | Justifikasi |
|----------|-----------|-------------|
| **Koherensi** | 3 | Alur logis atas-ke-bawah jelas: problem (developer memilih tanpa data) → gap (belum ada JMH + ArrayList vs HashMap + Java 17) → RQ (perbandingan performa) → hypothesis (pola perbedaan spesifik) → metrik (ns/op, bytes, ops/sec) → sistem (JMH + JOL) → eksperimen (comparison study dengan threat analysis). Semua koneksi terdokumentasi. |
| **Specificity** | 3 | Metrik sudah terdefinisi numerik: execution time dalam ns/op dengan CI 99%, memory dalam bytes via JOL, throughput dalam ops/sec. IV spesifik (ArrayList vs HashMap), operasi spesifik (5 CRUD), ukuran spesifik (10³–10⁶). Threshold signifikansi spesifik (p < 0.05, Cohen's d > 0.5). |
| **Feasibility** | 3 | Eksperimen feasible: JMH dan JOL adalah tools open-source mature, tidak memerlukan hardware khusus, timeline realistis (4 minggu untuk eksperimen + analisis). Dataset dapat di-generate dengan seed tetap. Tidak ada dependency eksternal yang kompleks. |
| **Rigor** | 3 | Metodologi rigorous: menggunakan JMH (standar industri untuk Java benchmarking), statistical testing (ANOVA + Tukey HSD + Bonferroni correction), threat analysis (12 ancaman dengan mitigasi), power analysis (target power 0.8), confidence interval 99%. Pre-registration metrik sebelum eksperimen. |

**Skor total:** **12 / 12** ✅

**Apakah proposal siap untuk fase eksekusi?** [X] Ya / [ ] Belum

> Jika belum, apa yang perlu diperbaiki?
> 
> **Proposal sudah siap untuk fase eksekusi.** Semua komponen (problem, gap, RQ, hypothesis, metrik, sistem, desain eksperimen) sudah terdefinisi dengan jelas dan konsisten. Berikutnya adalah fase implementasi (WS-09 sampai WS-16) untuk menjalankan eksperimen dan menganalisis hasil.

---

## RINGKASAN PROPOSAL LENGKAP

### Judul
**Analisis Perbandingan Performa Penggunaan ArrayList vs HashMap dalam Manajemen Data Objek pada Bahasa Pemrograman Java**

### Latar Belakang
Developer Java sering memilih struktur data koleksi berdasarkan intuisi atau kebiasaan tanpa panduan empiris yang valid. Pemilihan yang salah dapat menyebabkan performance bottleneck signifikan pada aplikasi production, terutama pada operasi data lookup dengan frekuensi tinggi. Studi existing yang membandingkan performa di Java (seperti Pujiono et al. 2024 untuk algoritma sorting) menggunakan metodologi benchmark yang lemah — `System.currentTimeMillis()` dengan single-run tanpa warmup, tanpa kontrol terhadap JIT compiler dan GC, dan tanpa uji statistik. Akibatnya, hasil tidak reproducible dan tidak bisa dijadikan dasar pengambilan keputusan teknis.

### Research Gap
Belum ada studi yang membandingkan ArrayList vs HashMap menggunakan **JMH (Java Microbenchmark Harness)** pada **Java 17 LTS** dengan **statistical significance testing** dan **multi-size dataset (10³–10⁶)**. Studi existing terbatas pada dataset kecil (<10K elemen), distribusi uniform random saja, dan tidak ada measurement akurat untuk memory footprint.

### Research Question
Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara `ArrayList<Person>` dan `HashMap<Integer, Person>` pada 5 operasi CRUD dasar (insert, search, update, delete, iterate) untuk 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶) di Java 17 LTS, diukur dengan JMH dan diuji signifikansinya secara statistik?

### Hipotesis
- **H₀:** Tidak ada perbedaan signifikan dalam performa (execution time, memory, throughput) antara ArrayList dan HashMap (p > 0.05)
- **H₁:** Ada perbedaan signifikan dengan pola:
  - HashMap lebih cepat pada operasi search (O(1) vs O(n)) dengan Cohen's d > 0.8
  - ArrayList lebih cepat pada operasi iterate (cache locality) dengan Cohen's d > 0.5
  - ArrayList lebih hemat memori pada dataset kecil (<10⁴) dengan perbedaan >10%

### Metodologi

**Variabel Independen (IV):**
- Struktur data: ArrayList<Person> vs HashMap<Integer, Person>
- Jenis operasi: insert, search, update, delete, iterate
- Ukuran dataset: 10³, 10⁴, 10⁵, 10⁶ elemen

**Variabel Dependen (DV):**
- Execution time (ns/op) dengan confidence interval 99%
- Memory footprint (bytes) via JOL
- Throughput (ops/sec)

**Variabel Kontrol (CV):**
- JVM: Java 17 LTS
- GC: G1GC
- Heap: 4GB fixed (`-Xms4g -Xmx4g`)
- Warmup: 5 × 1 second
- Measurement: 10 × 1 second
- Forks: 3 (3 JVM instance terpisah)

**Instrumen:**
- JMH (Java Microbenchmark Harness) v1.37 untuk timing
- JOL (Java Object Layout) v0.17 untuk memory measurement
- ANOVA + Tukey HSD + Bonferroni correction untuk analisis statistik

**Desain Eksperimen:**
- Tipe: Comparison study (ArrayList vs HashMap pada kondisi identik)
- Fairness: Dataset sama, preprocessing sama, environment sama, metrik sama
- Threat analysis: 12 ancaman validitas dengan mitigasi spesifik
- Statistical plan: Two-way ANOVA, p-value < 0.05, Cohen's d > 0.5, power 0.8

### Kontribusi
Perbandingan empiris performa ArrayList vs HashMap pada 5 operasi CRUD dasar dengan 4 ukuran dataset (10³–10⁶) menggunakan metodologi benchmark standar (JMH) pada Java 17 LTS, dengan uji signifikansi statistik (ANOVA + Tukey HSD) dan measurement akurat (JOL untuk memory). Hasil riset dapat dijadikan panduan empiris (decision matrix) untuk developer Java dalam memilih struktur data berdasarkan operasi dominan dan ukuran data.

### Timeline
- **Minggu 1:** Setup environment, implementasi benchmark harness
- **Minggu 2:** Eksperimen ArrayList (5 operasi × 4 ukuran × 3 forks = 60 runs)
- **Minggu 3:** Eksperimen HashMap (60 runs), data collection
- **Minggu 4:** Analisis statistik, visualisasi, penulisan laporan

### Output
- Raw benchmark data (CSV): 120 runs × 10 iterations = 1200 data points
- Aggregated statistics (JSON): mean, median, std dev, CI 99%, effect size
- Decision matrix: rekomendasi struktur data berdasarkan operasi dan ukuran
- Paper/laporan dengan hasil dan diskusi

---

## Refleksi

**Pertanyaan:** Dari seluruh proses WS-01 sampai WS-08, bagian mana yang paling mudah dan paling sulit? Mengapa? Apa yang akan dilakukan berbeda jika mengulang dari awal?

**Bagian termudah:** **WS-06 (System Design)**
> Karena JMH dan JOL adalah tools yang sudah mature dan well-documented. Mapping variabel ke komponen sistem straightforward: IV → benchmark methods, DV → JMH/JOL output, CV → JVM flags. Tidak ada ambiguitas dalam desain.

**Bagian tersulit:** **WS-03 (Literature Gap)**
> Karena memerlukan pencarian literatur yang sistematis dan analisis mendalam untuk mengidentifikasi gap yang valid. Harus membaca 5+ paper, memahami metodologi masing-masing, mengidentifikasi pola limitasi, dan memastikan gap yang diidentifikasi benar-benar ada (bukan asumsi). Juga sulit untuk menentukan kapan pencarian "cukup" — apakah sudah mencakup semua paper relevan atau masih ada yang terlewat?

**Yang akan dilakukan berbeda jika mengulang dari awal:**

1. **Mulai dengan literature search lebih awal** — Jangan tunggu WS-03 untuk mulai membaca paper. Mulai dari WS-01 untuk memahami landscape penelitian dan mengidentifikasi gap lebih cepat.

2. **Gunakan pre-registration** — Sebelum eksperimen, daftarkan RQ, hypothesis, metrik, dan analisis plan di OSF (Open Science Framework) untuk transparansi dan menghindari p-hacking.

3. **Buat integration map visual** — Diagram yang menunjukkan 6 koneksi kritis (problem → gap → RQ → metrik → sistem → eksperimen) akan membantu mengidentifikasi gap atau inkonsistensi lebih awal.

4. **Involve domain expert lebih awal** — Diskusikan dengan Java developer berpengalaman di WS-02 untuk memastikan problem statement benar-benar relevan dan gap yang diidentifikasi penting.

5. **Lakukan pilot eksperimen di WS-07** — Jangan langsung eksperimen penuh. Lakukan pilot dengan 1 operasi × 1 ukuran dataset untuk memastikan setup JMH bekerja dan tidak ada surprise di fase eksekusi.