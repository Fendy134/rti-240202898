# WS-02: Problem Statement

> **Bab 2 — Problem Formulation & System Context**

---

## Ringkasan Materi

### Problem Formation Model

Masalah riset melewati 5 tahap transformasi. Melompat langsung dari Reality ke Variable adalah kesalahan paling umum.

```
Reality → Observed Issue (Symptom) → Diagnosed Problem (Root Cause)
→ Researchable Problem (Scoped) → Measurable Variable (Operationalized)
```

### Topic ≠ Problem ≠ Research Problem

| Level | Contoh | Status |
|-------|--------|--------|
| **Topik** | Keamanan IoT | Terlalu luas, tidak bisa diuji |
| **Problem** | MQTT tidak terenkripsi | Spesifik tapi belum riset |
| **Research Problem** | Belum ada studi membandingkan overhead TLS 1.3 vs DTLS pada MQTT di IoT RAM < 64KB | Bisa dirancang eksperimennya |

### Symptom vs Root Cause

Apa yang diamati (gejala) ≠ mengapa terjadi (akar masalah). Gunakan **5 Whys** atau **Fishbone Diagram** untuk menggali.

Contoh: "User meninggalkan checkout" (symptom) → "Waktu loading > 8 detik karena API call sequential" (root cause).

### System Thinking

Setiap masalah riset TI harus terikat pada komponen sistem: **Input → Process → Output → Outcome → Constraints → Stakeholders**.

### Problem Quality Check

Masalah riset yang layak harus memenuhi 5 kriteria:
- **Clarity** — Satu orang membaca akan paham
- **Measurability** — Ada metrik kuantitatif
- **Relevance** — Penting untuk domain
- **Testability** — Bisa gagal (falsifiable)
- **Impact** — Ada kontribusi jika terjawab

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan | Menyelesaikan masalah (*solve*) | Memahami dan membuktikan (*understand & prove*) |
| Masalah | Bug, error, fitur belum ada | Gap dalam pengetahuan |
| Scope | Selesaikan semua yang perlu | Batasi agar bisa dibuktikan |
| Output | Working system | Evidence, paper, replicable findings |


### Istilah Penting

- **Problem Statement** — Formulasi tertulis: konteks sistem + gap + dampak + justifikasi
- **System Context** — Deskripsi lengkap: input, proses, output, outcome, constraints, stakeholders
- **Problem Drift** — Masalah "bermutasi" dari pendahuluan ke metodologi karena statement awal tidak presisi
- **Solution-First Thinking** — Memulai dari solusi tanpa masalah yang jelas — berbahaya dalam riset
- **Operational Definition** — Definisi variabel yang cukup jelas agar peneliti lain bisa mengukur hal yang sama

---

# WS-02: Problem Statement
**Mata Kuliah:** Riset Teknologi Informasi

---

##  Problem Statement Builder

**Domain & Konteks**
- **Domain:** Software Engineering & Data Structure Performance Analysis pada platform Java.
- **Konteks:** Pemilihan struktur data koleksi (`java.util.Collection`) yang tepat untuk manajemen data objek dalam aplikasi Java enterprise modern.

**System Context**
- **Input:** Dataset POJO `Person` (id, name, age, email) dengan ukuran bervariasi (10³, 10⁴, 10⁵, 10⁶ elemen).
- **Process:** Eksekusi 5 operasi CRUD dasar (insert, search, update, delete, iterate) menggunakan dua struktur data: `ArrayList<Person>` dan `HashMap<Integer, Person>`.
- **Output:** Pengukuran kuantitatif execution time (ns/op), memory footprint (bytes), dan throughput (ops/sec) untuk setiap kombinasi.
- **Outcome:** Panduan empiris berbasis data untuk developer Java dalam memilih struktur data yang sesuai dengan use case operasi dominan dan ukuran data.
- **Constraints:** Lingkungan single-threaded, JVM Java 17 dengan G1GC, hardware tetap, dataset acak dengan seed yang sama untuk reproducibility.
- **Stakeholders:** Java developer (terutama backend engineer), software architect yang mendesain data layer, dan technical lead yang membuat keputusan teknologi.

**Fenomena → Problem**
- **Fenomena yang diamati:** Developer Java sering memilih struktur data koleksi berdasarkan intuisi atau kebiasaan ("pakai ArrayList saja, lebih familiar") tanpa data empiris yang membandingkan performa pada berbagai operasi dan ukuran data.
- **Gejala (symptom) yang terukur:** Banyak aplikasi Java mengalami performance bottleneck pada operasi data layer yang seharusnya bisa dihindari dengan pemilihan struktur data yang lebih sesuai (misalnya O(n) linear search di ArrayList ketika HashMap lookup O(1) tersedia).
- **Masalah yang didiagnosis:** Belum ada studi pembanding **ArrayList vs HashMap** yang menggunakan metodologi benchmark standar (JMH) pada Java 17+ dengan uji statistik. Studi existing (seperti Pujiono dkk 2024 untuk algoritma sorting) menggunakan `System.currentTimeMillis()` single-run tanpa kontrol JIT/GC, sehingga hasilnya tidak reliable.
- **Masalah riset (researchable):** Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara `ArrayList<Person>` dan `HashMap<Integer, Person>` pada 5 operasi CRUD dasar untuk 4 ukuran dataset (10³–10⁶) di Java 17, diukur dengan JMH dan diuji signifikansinya secara statistik?
- **Variabel yang terukur:** Execution time (ns/op), memory footprint (bytes via JOL), throughput (ops/sec), dengan IV: jenis struktur data, jenis operasi, dan ukuran dataset.

**Problem Quality Check**
- [X] **Clarity** — Masalah spesifik: perbandingan dua struktur data konkret pada operasi tertentu.
- [X] **Measurability** — Tiga metrik kuantitatif dengan satuan jelas (ns/op, bytes, ops/sec).
- [X] **Relevance** — ArrayList dan HashMap adalah dua struktur data paling banyak dipakai di ekosistem Java.
- [X] **Testability** — Hipotesis bisa difalsifikasi (misal: "HashMap lebih cepat di search" bisa salah jika data menunjukkan sebaliknya pada ukuran tertentu).
- [X] **Impact** — Memberikan panduan empiris yang dapat dipakai langsung oleh developer dalam decision making.

**Problem Statement (1 Paragraf):**
Developer Java sering memilih struktur data koleksi berdasarkan intuisi tanpa panduan empiris yang valid, padahal pemilihan yang salah dapat menyebabkan performance bottleneck yang signifikan pada aplikasi production. Studi existing yang membandingkan performa di Java (seperti Pujiono dkk 2024 untuk algoritma sorting) menggunakan metodologi benchmark yang lemah — `System.currentTimeMillis()` dengan single-run tanpa warmup, tanpa kontrol terhadap JIT compiler dan GC, dan tanpa uji statistik. Akibatnya, hasil tidak reproducible dan tidak bisa dijadikan dasar pengambilan keputusan teknis. Penelitian ini bertujuan menghasilkan analisis perbandingan performa **ArrayList vs HashMap** pada 5 operasi CRUD dasar (insert, search, update, delete, iterate) untuk 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶) menggunakan **Java Microbenchmark Harness (JMH)** sebagai instrumen standar, dengan uji signifikansi statistik (ANOVA + Tukey HSD), pada Java 17 LTS.

---

##  Latihan 1 — Dari Topik ke Masalah Riset

**Topik awal:** Performa Struktur Data di Java.

| Tahap | Hasil |
|-------|-------|
| **Reality** | Aplikasi Java enterprise mengalami latency tinggi pada operasi data lookup yang frekuensinya tinggi. |
| **Observed Issue (Symptom)** | Profiling menunjukkan operasi `list.contains(x)` di `ArrayList` menjadi hotspot pada list dengan >10⁴ elemen. |
| **Diagnosed Problem (Root Cause)** | Developer memilih `ArrayList` sebagai default karena familiar, tanpa mempertimbangkan kompleksitas operasi: `contains()` di `ArrayList` adalah O(n), sementara `HashMap.containsKey()` adalah O(1) average case. |
| **Researchable Problem** | Belum ada studi yang membandingkan performa `ArrayList` vs `HashMap` untuk 5 operasi CRUD dasar dengan metodologi benchmark standar (JMH) dan uji statistik pada Java 17. |
| **Measurable Variable** | Execution time (ns/op), memory footprint (bytes), throughput (ops/sec). |

**Apakah terjebak solution-first thinking?** [ ] Ya / [X] Tidak  
> **Justifikasi:** Riset dimulai dari fenomena nyata (latency tinggi, profiling hotspot) dan gap metodologi pada studi existing, bukan dari keinginan menggunakan tool tertentu. JMH dipilih bukan karena ingin pakai JMH, tapi karena tool ini menjawab kelemahan metodologi pada studi sebelumnya.

---

##  Latihan 2 — System Context Decomposition

| Komponen | Deskripsi |
|----------|----------|
| **Input** | Dataset POJO `Person` (id: int, name: String, age: int, email: String) dengan 4 ukuran: 10³, 10⁴, 10⁵, 10⁶ elemen, di-generate dengan `Random` ber-seed tetap untuk reproducibility. |
| **Process** | Eksekusi 5 operasi CRUD (insert, search, update, delete, iterate) pada `ArrayList<Person>` dan `HashMap<Integer, Person>` melalui JMH benchmark methods (`@Benchmark`). |
| **Output** | File CSV dan JSON berisi raw measurement: execution time per operasi (ns/op), memory footprint (bytes), throughput (ops/sec), dengan confidence interval 99%. |
| **Outcome** | Panduan empiris (decision matrix) untuk developer: "jika operasi dominan = search dan ukuran data > 10⁴, gunakan HashMap karena X% lebih cepat dengan signifikansi p < 0.05". |
| **Constraints** | Single-threaded, Java 17 LTS, G1GC, heap 4GB fixed (`-Xms4g -Xmx4g`), 5 warmup × 1s + 10 measurement × 1s, 3 forks per benchmark. |
| **Stakeholders** | Java backend developer, software architect, technical lead — siapapun yang membuat keputusan struktur data di kode Java. |

**Komponen mana yang paling relevan dengan masalah riset?** **Process** — karena variabel independen (jenis struktur data dan operasi) dan dependen (waktu, memori) keduanya berada di tahap eksekusi. Process inilah yang dimanipulasi dan diukur.

---

##  Latihan 3 — Problem Quality Check

| Kriteria | Skor (1-5) | Justifikasi |
|----------|-----------|-------------|
| **Clarity** | 5 | Fokus pada perbandingan dua struktur data konkret (ArrayList vs HashMap) untuk 5 operasi spesifik pada 4 ukuran data tertentu. |
| **Measurability** | 5 | Tiga metrik kuantitatif dengan satuan SI yang jelas: ns/op, bytes, ops/sec. Diukur dengan instrumen standar (JMH + JOL). |
| **Relevance** | 5 | ArrayList dan HashMap adalah dua dari struktur data paling banyak dipakai dalam ekosistem Java (lihat statistik penggunaan `java.util` di GitHub). |
| **Testability** | 5 | Setiap hipotesis (misal H1: HashMap lebih cepat di search) bisa difalsifikasi dengan data benchmark + uji ANOVA. |
| **Impact** | 4 | Memberikan panduan empiris yang langsung dapat dipakai developer. Skor 4 (bukan 5) karena terbatas pada single-threaded — concurrent scenario perlu studi lanjutan. |

**Skor total:** **24 / 25**

**Problem statement versi final (1 paragraf):**
Pemilihan struktur data koleksi di Java sering didasarkan pada intuisi tanpa panduan empiris yang valid, sementara studi pembanding existing menggunakan metodologi benchmark yang lemah (`System.currentTimeMillis()`, single-run, tanpa kontrol JIT/GC, tanpa uji statistik) sehingga hasilnya tidak reproducible. Penelitian ini melakukan analisis komparatif performa **`ArrayList<Person>`** dan **`HashMap<Integer, Person>`** pada 5 operasi CRUD dasar (insert, search, update, delete, iterate) dengan 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶) menggunakan **Java Microbenchmark Harness (JMH)** sebagai instrumen pengukuran standar, **JOL (Java Object Layout)** untuk memory footprint, dan **ANOVA + Tukey HSD post-hoc** untuk uji signifikansi pada Java 17 LTS. Kontribusi utama adalah panduan empiris (decision matrix) berbasis bukti statistik untuk decision making developer.

---

##  Refleksi

**Pertanyaan:** Apa perbedaan antara masalah dalam coding sehari-hari (bug, error) dengan masalah riset?

**Jawaban:** Perbedaan paling fundamental terletak pada **tujuan dan output**. Masalah coding bersifat **reaktif dan corrective** — ada bug yang menghambat sistem, target adalah menghilangkan bug agar sistem berfungsi. Masalah riset bersifat **eksploratif dan generative** — ada gap dalam pengetahuan, target adalah menghasilkan bukti empiris yang dapat divalidasi oleh komunitas. Dalam konteks riset ini, jika developer mengeluh "aplikasi saya lambat di operasi search", itu adalah masalah engineering yang diselesaikan dengan profiling dan refactoring spesifik. Tetapi pertanyaan "apakah HashMap secara signifikan lebih cepat dari ArrayList untuk search di Java 17?" adalah masalah riset, karena membutuhkan eksperimen terkontrol, pengukuran berulang, uji statistik, dan dokumentasi yang reproducible. Output engineering adalah patch atau commit; output riset adalah temuan yang dapat di-cite, di-replikasi, dan di-bangun di atasnya oleh peneliti lain.