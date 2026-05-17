# WS-04: Research Question & Hypothesis

> **Bab 4 — Research Question, Contribution & Hypothesis**

---

## Ringkasan Materi

### RQ Bukan Pertanyaan Biasa

Research Question yang baik secara implisit mengandung cetak biru eksperimen: subjek, baseline, metrik, domain, dataset.

| Kualitas | Contoh |
|----------|--------|
| **Buruk** | "Bagaimana pengaruh deep learning terhadap deteksi malware?" |
| **Baik** | "Apakah CNN menghasilkan F1-Score lebih tinggi dari RF pada CIC-MalMem-2022?" |

Perbedaan: RQ yang baik menyebutkan **metode spesifik**, **metrik terukur**, **baseline**, dan **dataset**.

### Tiga Jenis RQ

| Jenis | Pola | Kebutuhan |
|-------|------|----------|
| **Comparison** | A vs B → mana lebih baik? | ≥ 2 metode, metrik sama |
| **Improvement** | A' vs A → modifikasi lebih baik? | Pre/post, bukti perbaikan |
| **Exploratory** | Faktor X₁...Xₙ → pengaruh terhadap Y? | Multi-variabel, korelasi/regresi |

### Contribution Statement

Tiga jenis kontribusi: **Improvement** (metode terbukti lebih baik), **Comparison** (perbandingan sistematis yang belum ada), **Novel Approach** (pendekatan baru). Kontribusi harus terhubung langsung dengan gap — kontribusi tanpa gap = klaim tanpa justifikasi.

### Hypothesis H₀ / H₁

- **H₀** (Null) = Tidak ada perbedaan signifikan — asumsi default, harus dibuktikan salah
- **H₁** (Alternative) = Ada perbedaan signifikan — diterima hanya jika H₀ ditolak
- Harus **falsifiable**, mengandung **metrik terukur**, dirumuskan **SEBELUM eksperimen**

### Rantai Operasionalisasi

```
RQ → Variable → Metric → Data → Analysis
```

Jika rantai ini tidak lengkap, RQ belum mature. Bi-directional: RQ yang tidak bisa jadi hipotesis testable harus direvisi mundur.

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan pertanyaan | Apa yang harus dibangun? | Apa yang harus dibuktikan? |
| Bentuk jawaban | Sistem yang berfungsi | Bukti empiris terukur |
| Sukses diukur oleh | User satisfaction, uptime | Signifikansi statistik, effect size |
| Jika gagal | Debug dan perbaiki | Laporkan, analisis mengapa |

### Istilah Penting

- **Research Question (RQ)** — Pertanyaan spesifik: variabel terukur + metrik + konteks
- **Contribution Statement** — Apa yang diketahui setelah riset selesai yang sebelumnya belum ada
- **H₀ / H₁** — Null vs Alternative Hypothesis
- **Falsifiability** — Kondisi hipotesis ditolak harus bisa didefinisikan sebelum eksperimen
- **Operationalization** — Proses mewujudkan konsep abstrak menjadi variabel terukur

---

# WS-04: Research Question & Hypothesis
**Mata Kuliah:** Riset Teknologi Informasi

---

## RQ-CONTRIBUTION-HYPOTHESIS

**Gap Statement:**  
Belum ada studi yang membandingkan ArrayList vs HashMap menggunakan JMH pada Java 17 LTS dengan statistical significance testing dan multi-size dataset (10³–10⁶). Studi existing menggunakan metodologi lemah (`System.currentTimeMillis()` single-run) sehingga hasil tidak reproducible.

**Research Question:**

**Tipe:** [X] Comparison  [ ] Improvement  [ ] Exploratory

**Formulasi:**  
Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara `ArrayList<Person>` dan `HashMap<Integer, Person>` pada 5 operasi CRUD dasar (insert, search, update, delete, iterate) untuk 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶) di Java 17 LTS, diukur dengan JMH dan diuji signifikansinya secara statistik?

**Variabel IV:**  
- Struktur data: ArrayList<Person> vs HashMap<Integer, Person>
- Jenis operasi: insert, search, update, delete, iterate
- Ukuran dataset: 10³, 10⁴, 10⁵, 10⁶ elemen

**Variabel DV:**  
- Execution time (ns/op)
- Memory footprint (bytes)
- Throughput (ops/sec)

**Metrik:**  
- Durasi execution time per operasi (ns/op) dengan confidence interval 99%
- Total memory footprint (bytes) via JOL
- Throughput (ops/sec)
- Effect size (Cohen's d) untuk perbandingan pairwise

**Dataset:**  
Dataset POJO `Person` (id: int, name: String, age: int, email: String) dengan 4 ukuran, di-generate dengan `Random` ber-seed tetap untuk reproducibility.

**Baseline:**  
- Gorelick & Ozsvald (2020) — JMH best practice untuk Java benchmarking
- Oracle Java Docs (2023) — Theoretical complexity reference

**Quality Check RQ:**
- [X] Variabel spesifik (ArrayList vs HashMap, 5 operasi, 4 ukuran)
- [X] Metrik jelas (ns/op, bytes, ops/sec dengan confidence interval)
- [X] Baseline ada (Gorelick & Ozsvald 2020, Oracle Docs)
- [X] Konteks disebutkan (Java 17 LTS, G1GC, single-threaded)
- [X] Memerlukan eksperimen (bukan hanya survei literatur)

---

**Contribution Statement:**

**Apa yang baru diketahui:**  
Perbandingan empiris performa ArrayList vs HashMap pada 5 operasi CRUD dasar dengan 4 ukuran dataset (10³–10⁶) menggunakan metodologi benchmark standar (JMH) pada Java 17 LTS, dengan uji signifikansi statistik (ANOVA + Tukey HSD) dan measurement akurat (JOL untuk memory).

**Jenis kontribusi:**  
[X] Comparison  [ ] Improvement  [ ] Novel approach

**Gap yang diisi:**  
Mengisi gap metodologi dan konteks pada studi existing yang menggunakan `System.currentTimeMillis()` single-run tanpa warmup, serta gap data pada evaluasi hanya <10K elemen. Hasil riset ini dapat dijadikan panduan empiris (decision matrix) untuk developer Java dalam memilih struktur data berdasarkan operasi dominan dan ukuran data.

---

**Hypothesis Pair:**

**H₀ (Null Hypothesis):**  
Tidak ada perbedaan signifikan dalam performa (execution time, memory footprint, throughput) antara ArrayList<Person> dan HashMap<Integer, Person> pada 5 operasi CRUD dasar untuk 4 ukuran dataset (10³–10⁶) di Java 17 LTS (p > 0.05).

**H₁ (Alternative Hypothesis):**  
Ada perbedaan signifikan dalam performa antara ArrayList dan HashMap pada minimal satu kombinasi operasi × ukuran dataset, dengan pola spesifik:
- H1a: HashMap lebih cepat pada operasi search (O(1) vs O(n)) dengan effect size Cohen's d > 0.8
- H1b: ArrayList lebih cepat pada operasi iterate (cache locality) dengan effect size Cohen's d > 0.5
- H1c: ArrayList lebih hemat memori pada dataset kecil (<10⁴) dengan perbedaan >10%

**Threshold Signifikansi:**  
- p-value < 0.05 untuk menolak H₀
- Effect size (Cohen's d) > 0.5 untuk dianggap praktis signifikan
- Confidence interval 99% untuk semua measurement

**Justifikasi Threshold:**  
- p < 0.05 adalah standar signifikansi statistik dalam penelitian empiris
- Cohen's d > 0.5 adalah medium effect size yang dianggap praktis signifikan dalam konteks performa (perbedaan >50% bisa mempengaruhi keputusan teknis)
- Confidence interval 99% dipilih karena JMH measurement bisa bervariasi akibat JIT/GC, perlu confidence yang tinggi

---

# Latihan 1 — Dari Gap ke RQ

**Gap dari WS-03:**  
Belum ada studi yang membandingkan ArrayList vs HashMap menggunakan JMH pada Java 17 LTS dengan statistical significance testing dan multi-size dataset (10³–10⁶).

**RQ versi pertama (tulis bebas):**
> Bagaimana performa ArrayList dibandingkan HashMap di Java?

**Evaluasi RQ:**

| Komponen | Ada? | Isi |
|:---------|:----:|:---|
| Metode spesifik | Tidak | Perlu: JMH, bukan hanya timing biasa |
| Metrik terukur | Tidak | Perlu: ns/op, bytes, ops/sec, bukan hanya "lebih cepat" |
| Baseline | Tidak | Perlu: dibanding dengan apa? Gorelick & Ozsvald 2020? |
| Dataset/konteks | Tidak | Perlu: Java 17, ukuran data berapa, operasi apa |

**Tipe RQ:** [X] Comparison / [ ] Improvement / [ ] Exploratory

**RQ versi revisi (setelah evaluasi):**
> Bagaimana perbedaan performa kuantitatif (execution time, memory footprint, throughput) antara ArrayList<Person> dan HashMap<Integer, Person> pada 5 operasi CRUD dasar (insert, search, update, delete, iterate) untuk 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶) di Java 17 LTS, diukur dengan JMH dan diuji signifikansinya secara statistik?

---

# Latihan 2 — Hypothesis Pair

**RQ:** Bagaimana perbedaan performa ArrayList vs HashMap pada 5 operasi CRUD untuk 4 ukuran dataset di Java 17?

| Komponen | Isi |
|:---------|:---|
| H₀ | Tidak ada perbedaan signifikan dalam performa (execution time, memory, throughput) antara ArrayList dan HashMap pada 5 operasi CRUD untuk 4 ukuran dataset (p > 0.05) |
| H₁ | Ada perbedaan signifikan pada minimal satu kombinasi operasi × ukuran dataset, dengan pola: HashMap lebih cepat di search (O(1) vs O(n)), ArrayList lebih cepat di iterate (cache locality), ArrayList lebih hemat memori pada dataset kecil |
| Metrik | Execution time (ns/op), memory footprint (bytes), throughput (ops/sec) |
| Threshold | p-value < 0.05, effect size Cohen's d > 0.5, confidence interval 99% |
| Justifikasi threshold | p < 0.05 standar statistik, Cohen's d > 0.5 medium effect size (praktis signifikan), CI 99% karena JIT/GC variabilitas tinggi |

**Apakah hipotesis ini falsifiable?** [X] Ya / [ ] Tidak

> **Bagaimana cara membuktikannya salah?**  
> Jika hasil eksperimen menunjukkan:
> - p-value > 0.05 untuk semua kombinasi operasi × ukuran dataset, ATAU
> - Effect size Cohen's d < 0.5 untuk semua kombinasi, ATAU
> - Confidence interval 99% overlap antara ArrayList dan HashMap
> 
> Maka H₀ tidak ditolak dan H₁ ditolak. Dengan demikian, klaim bahwa ada perbedaan signifikan performa tidak terbukti secara statistik.

---

# Latihan 3 — Rantai Operasionalisasi

**Lengkapi rantai dari RQ hingga metode analisis:**

| Tahap | Isi |
|:------|:---|
| **RQ** | Bagaimana perbedaan performa ArrayList vs HashMap pada 5 operasi CRUD untuk 4 ukuran dataset di Java 17? |
| **Variable (IV)** | (1) Struktur data: ArrayList<Person> vs HashMap<Integer, Person>, (2) Operasi: insert, search, update, delete, iterate, (3) Ukuran data: 10³, 10⁴, 10⁵, 10⁶ |
| **Variable (DV)** | (1) Execution time (ns/op), (2) Memory footprint (bytes), (3) Throughput (ops/sec) |
| **Metric** | Durasi execution time per operasi dengan confidence interval 99%, total memory via JOL, throughput dalam ops/sec |
| **Data source** | Dataset POJO Person (id, name, age, email) dengan 4 ukuran, di-generate dengan Random ber-seed tetap |
| **Measurement tool** | JMH (Java Microbenchmark Harness) v1.37 untuk timing, JOL (Java Object Layout) v0.17 untuk memory |
| **Experimental setup** | 5 warmup × 1s, 10 measurement × 1s, 3 forks, single-threaded, Java 17 LTS, G1GC, heap 4GB fixed |
| **Analysis method** | Two-way ANOVA (IV: struktur data × operasi, DV: execution time), post-hoc Tukey HSD untuk pairwise comparison, effect size Cohen's d |
| **Statistical test** | ANOVA p-value < 0.05 untuk signifikansi, Cohen's d > 0.5 untuk practical significance |

**Apakah rantai lengkap?** [X] Ya / [ ] Tidak

> Jika tidak, tahap mana yang perlu direvisi? Rantai sudah lengkap dari RQ hingga metode analisis. Setiap tahap terhubung logis tanpa lompatan.

---

# Refleksi

**Pertanyaan:** Ambil satu judul skripsi/paper yang pernah dibaca. Coba ekstrak RQ-nya. Apakah RQ tersebut memenuhi semua komponen (metode, metrik, baseline, konteks)? Jika tidak, apa yang hilang?

**Judul:** Perbandingan Efisiensi Memori dan Waktu Komputasi pada 7 Algoritma Sorting Menggunakan Bahasa Pemrograman Java (Pujiono et al., 2024)

**RQ yang diekstrak:**  
> Apakah algoritma sorting tertentu lebih efisien dalam hal waktu komputasi dan penggunaan memori dibandingkan algoritma lain?

**Komponen yang ada:**
- [X] Metode: 7 algoritma sorting (Bubble, Insertion, Selection, Shell, Quick, Merge, Heap)
- [X] Metrik: waktu komputasi dan memori
- [ ] Baseline: tidak jelas (dibanding dengan apa? Algoritma mana yang baseline?)
- [ ] Konteks: Java disebutkan, tapi versi tidak disebutkan, ukuran data hanya 3 level (100, 1K, 10K)

**Komponen yang hilang:**
- **Baseline tidak jelas** — Seharusnya: "dibanding dengan Shell Sort sebagai baseline" atau "dibanding dengan algoritma O(n log n) terbaik"
- **Metrik tidak spesifik** — Seharusnya: "execution time dalam ns/op dengan confidence interval 99%" bukan hanya "waktu komputasi"
- **Konteks terbatas** — Seharusnya: "Java 8/11/17, tipe data int, distribusi uniform random, single-threaded" bukan hanya "Java"
- **Tidak ada statistical test** — Seharusnya: "dengan ANOVA p < 0.05 untuk signifikansi" bukan hanya perbandingan nilai

**Kesimpulan:**  
RQ dalam paper Pujiono et al. (2024) masih terlalu umum dan perlu diperkuat dengan spesifikasi metrik, baseline yang jelas, konteks yang detail, dan rencana analisis statistik agar menjadi research question yang matang dan testable. Ini adalah contoh RQ yang "buruk" menurut standar riset modern.