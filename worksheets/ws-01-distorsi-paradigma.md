# WS-01: Distorsi & Paradigma

> **Bab 1 — Research Mindset in IT**

---

## Ringkasan Materi

### Research Trust Model

Pengetahuan ilmiah tidak muncul langsung dari kenyataan. Ia melewati **6 tahap transformasi** yang masing-masing rawan distorsi:

```
Reality → Data → Processing → Analysis → Inference → Knowledge
```

Etika mencegah distorsi yang disengaja (fabrikasi, cherry-picking). Validitas mendeteksi distorsi yang tidak disengaja (confounding variable, sampling bias).

### Tiga Jenis Validitas

| Jenis | Pertanyaan | Contoh Ancaman |
|-------|-----------|----------------|
| **Internal Validity** | Apakah hubungan kausal benar ada? | Confounding variable |
| **External Validity** | Apakah bisa digeneralisasi? | Dataset terlalu homogen |
| **Construct Validity** | Apakah mengukur hal yang benar? | Metrik tidak sesuai klaim |

### Paradigma Riset

Mata kuliah ini menggunakan pendekatan **Positivist** (fenomena TI bisa diukur objektif melalui eksperimen terkontrol) diperkuat **Design Science Research** (artefak dibuat sebagai instrumen pengujian hipotesis, bukan tujuan akhir).

### Mode Berpikir Peneliti

**Curious** (mempertanyakan fenomena) → **Critical** (mengevaluasi klaim berdasarkan bukti) → **Systematic** (merancang investigasi terstruktur dan reproducible).

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan | Membuat sistem yang bekerja | Menghasilkan pengetahuan yang valid |
| Pertanyaan khas | "Bagaimana membuatnya jalan?" | "Apakah klaim ini benar?" |
| Ukuran sukses | Sistem berfungsi, client puas | Hipotesis terjawab, temuan tervalidasi |
| Kegagalan | Harus dihindari | Harus dilaporkan (negative result = kontribusi) |

### Istilah Penting

- **Research Mindset** — Pola pikir yang menuntut bukti dan mempertanyakan asumsi
- **Research Ethics** — Prinsip perilaku: kejujuran, objektivitas, keterbukaan, akuntabilitas
- **HARKing** — Hypothesizing After Results are Known — merumuskan hipotesis setelah melihat data
- **Falsifiability** — Hipotesis harus bisa dibuktikan salah

---

# WS-01: Distorsi & Paradigma
**Mata Kuliah:** Riset Teknologi Informasi

---

##  Research Mindset Self-Assessment

**Nama Peneliti:** [Nama Anda]  
**Tanggal:** [Tanggal Pengisian]

1. **Ketika membaca klaim "ArrayList 30% lebih cepat dari HashMap":**
   - **Pertanyaan pertama saya:** "Untuk operasi apa? Pada ukuran data berapa? Apakah benchmark menggunakan JMH atau hanya `System.currentTimeMillis()` tanpa warmup?"
   - **Data yang dibutuhkan untuk verifikasi:** Kode benchmark lengkap, versi JVM, konfigurasi GC, ukuran dataset, jenis operasi (insert/search/update/delete/iterate), jumlah warmup & measurement iterations, dan distribusi raw data (mean ± std dev, median, percentile 95/99).

2. **Posisi paradigma:**
   - **Pendekatan:** [X] Positivis  [ ] Interpretivis  [ ] Design Science  [ ] Mixed
   - **Alasan:** Riset ini mengukur fenomena objektif (execution time, memory footprint) melalui eksperimen terkontrol dengan variabel yang dapat dimanipulasi (struktur data, operasi, ukuran data) dan diukur secara kuantitatif. Meskipun ada elemen Design Science (benchmark harness sebagai instrumen), fokus utama adalah **pengukuran perbandingan** struktur data yang sudah ada, bukan membangun artefak baru.

3. **Identifikasi distorsi:**
   - **Asumsi tersembunyi:** JVM sudah "warmed up" sehingga hasil benchmark stabil — padahal cold start sangat berbeda dari steady state akibat JIT compilation yang non-deterministik.
   - **Sumber bias potensial:** Penggunaan data acak terdistribusi uniform, padahal real-world data sering memiliki pola tertentu (skewed distribution, hash collision pattern, locality of reference).
   - **Langkah mitigasi:** Menggunakan JMH dengan ≥5 warmup iterations, menguji 4 ukuran dataset (10³, 10⁴, 10⁵, 10⁶), melaporkan confidence interval 99%, dan menjalankan multiple forks untuk menangkap variabilitas antar JVM instance.

4. **Komitmen etika:**
   - **Data yang tidak akan dimanipulasi:** Hasil benchmark mentah JMH (termasuk run yang menunjukkan ArrayList lebih lambat dari HashMap), tidak akan melakukan cherry-picking demi narasi yang lebih kuat.
   - **Batasan yang diakui sejak awal:** Hasil hanya berlaku untuk Java 17 dengan G1GC pada hardware spesifik yang digunakan, tidak mencakup concurrent access (ConcurrentHashMap), dan terbatas pada operasi CRUD dasar dengan tipe data POJO sederhana.

---

##  Latihan 1 — Identifikasi Distorsi

**Paper yang dipilih:**
> **Judul:** Perbandingan Efisiensi Memori dan Waktu Komputasi pada 7 Algoritma Sorting Menggunakan Bahasa Pemrograman Java  
> **Penulis (Tahun):** Imam Prayogo Pujiono, Rahmawan Bagus Trianto, Fida Maisa Hana (2024)

| Tahap | Apa yang Dilakukan | Potensi Distorsi |
|-------|-------------------|-----------------|
| **Reality → Data** | Mengukur waktu eksekusi sorting dengan `System.currentTimeMillis()` dan memory usage dengan `Runtime.getRuntime().totalMemory() - freeMemory()`. | **Measurement Bias:** `currentTimeMillis()` memiliki resolusi rendah (~15ms di Windows), tidak cocok untuk operasi cepat di bawah millisecond. Method `totalMemory() - freeMemory()` mengukur heap usage saat itu — bisa salah tangkap karena GC yang non-deterministik. |
| **Data → Processing** | Menjalankan setiap algoritma sekali per ukuran dataset (100, 1.000, 10.000 elemen) tanpa warmup. | **Cold Start Bias:** Eksekusi pertama lambat karena JVM belum melakukan JIT optimization. Tanpa warmup iterations, hasil mencampur fase interpreter dan compiled code, sehingga tidak mencerminkan steady-state performance. |
| **Processing → Analysis** | Membandingkan rata-rata waktu dan memori dari satu run per algoritma per ukuran data. | **Statistical Invalidity:** Single-run tidak menangkap variabilitas. Tidak ada confidence interval, standard deviation, atau uji statistik (ANOVA/t-test) yang dilaporkan untuk mendukung klaim "lebih cepat". |
| **Analysis → Inference** | Menyimpulkan Shell Sort tercepat untuk 100-1.000 data, Heap Sort untuk 10.000 data. | **Confounding Variable:** Perbedaan performa bisa disebabkan oleh GC pause atau OS scheduler yang tidak dikontrol, bukan murni karakteristik algoritma. |
| **Inference → Knowledge** | Mengklaim hasil berlaku umum untuk "sorting di Java". | **Generalization Bias:** Hasil hanya valid untuk versi Java yang digunakan (tidak disebut), tipe primitif `int`, dan distribusi acak uniform. Tidak mencakup nearly-sorted data, data dengan banyak duplicates, atau objek kompleks. |

**Distorsi paling besar di tahap:** **Data → Processing**

**Dua distorsi spesifik yang teridentifikasi:**
1. **Inadequate Benchmarking Methodology:** Tidak menggunakan framework benchmark standar (JMH) yang menangani warmup, dead code elimination, constant folding, dan loop unrolling. Akibatnya, JIT compiler bisa mengoptimasi kode benchmark dengan cara yang membuat hasil tidak mencerminkan performa sebenarnya di production.
2. **Single-Run Fallacy:** Mengambil kesimpulan dari satu eksekusi tanpa repetisi atau uji signifikansi statistik. Performa JVM bervariasi antar run karena non-deterministic JIT compilation dan GC, sehingga satu measurement tidak cukup untuk klaim performa yang reliable.

---

##  Latihan 2 — Analisis Kasus Etika

**Skenario:** Peneliti menjalankan benchmark JMH 20 kali, tetapi hanya melaporkan 5 run terbaik di mana ArrayList menang melawan HashMap pada operasi search.

| Perspektif | Analisis |
|------------|---------|
| **Kejujuran ilmiah** | Ini adalah bentuk **cherry-picking** — memilih data yang mendukung hipotesis dan menyembunyikan data yang bertentangan. Peneliti harus melaporkan **semua** run atau minimal statistik agregat (mean, median, std dev, min/max). |
| **Transparansi** | Pembaca berhak tahu bahwa ada 15 run lain yang tidak dilaporkan. Tanpa informasi ini, mereka tidak bisa menilai reliabilitas hasil atau melakukan replikasi. |
| **Peer review** | Reviewer tidak bisa mendeteksi manipulasi ini tanpa akses ke raw data. Jika terungkap setelah publikasi, paper bisa di-retract dan merusak reputasi peneliti serta institusinya. |

**Keputusan akhir dan justifikasi:**
> Laporkan **semua 20 run** atau minimal statistik deskriptif lengkap (mean ± std dev, median, min/max, percentile 95/99). Jika ada outlier ekstrem yang jelas penyebabnya (misal GC pause >500ms terdeteksi di GC log), boleh dihapus **dengan justifikasi eksplisit dan dokumentasi raw data sebagai supplementary material**. JMH sendiri sudah menangani outlier detection otomatis dan melaporkan confidence interval — manfaatkan fitur ini, jangan dimatikan demi narasi yang lebih kuat.

---

##  Latihan 3 — Posisi Paradigma

**Topik riset:** Analisis Perbandingan Performa ArrayList vs HashMap dalam Manajemen Data Objek pada Java.

| Kriteria | Positivis | Interpretivis | Design Science |
|----------|-----------|---------------|----------------|
| **Kesesuaian (1–5)** | 5 | 1 | 3 |
| **Jenis data** | Kuantitatif: execution time (ns/op), memory footprint (bytes), throughput (ops/sec). | Kualitatif: persepsi developer tentang readability/maintainability — tidak relevan untuk pertanyaan performa. | Pengembangan benchmark harness sebagai artefak — relevan tapi sebagai instrumen, bukan kontribusi utama. |
| **Limitasi** | Tidak menangkap aspek kualitatif seperti developer experience atau code maintainability. | Tidak cocok untuk pertanyaan "mana yang lebih cepat?" yang membutuhkan pengukuran objektif. | Bisa mengaburkan fokus — riset ini bukan tentang "cara membuat benchmark tool yang baik" tetapi "perbedaan performa ArrayList vs HashMap". |

**Paradigma yang dipilih:** **Positivist**  
**Alasan:** Riset ini mengukur fenomena objektif (performa struktur data) melalui eksperimen terkontrol. Variabel independen (struktur data, operasi, ukuran data) dapat dimanipulasi secara sistematis, dan variabel dependen (waktu, memori) dapat diukur secara kuantitatif menggunakan instrumen standar (JMH). Meskipun ada elemen Design Science (benchmark harness), itu berfungsi sebagai **instrumen pengukuran**, bukan kontribusi utama riset. Kontribusi inti adalah **comparative empirical analysis**, bukan artifact creation.

---

##  Refleksi

**Jawaban:**
> Sebelum ini, saya cenderung menerima klaim performa seperti "X lebih cepat 30%" tanpa mempertanyakan metodologi pengukurannya. Setelah memahami rantai distorsi, saya menyadari bahwa **bagaimana** angka itu diperoleh sama pentingnya dengan angka itu sendiri. Pertanyaan utama saya kini adalah: **"Apakah benchmark ini menggunakan metodologi valid (JMH dengan warmup, multiple forks, statistical testing), atau hanya `System.currentTimeMillis()` yang dijalankan sekali tanpa kontrol terhadap JIT/GC?"** Saya juga akan lebih waspada terhadap **confounding variables** seperti GC pause, OS scheduler, dan CPU thermal throttling yang bisa mempengaruhi hasil tetapi sering tidak dikontrol dalam eksperimen performa.