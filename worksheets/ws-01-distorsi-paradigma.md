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

**Nama Peneliti:** Fendy Agustian  
**Tanggal:** 9 April 2026 

1. **Ketika membaca klaim "metode X 95% akurat":**
   - **Pertanyaan pertama saya:** "Bagaimana komposisi dataset yang digunakan dan apakah ada indikasi *overfitting* atau *imbalanced data*?"
   - **Data yang dibutuhkan untuk verifikasi:** *Confusion Matrix*, rincian pembagian data *training/testing*, dan nilai metrik lain seperti *Precision, Recall,* dan *F1-Score*.

2. **Posisi paradigma:**
   - **Pendekatan:** [ ] Positivis  [ ] Interpretivis  [X] Design Science  [ ] Mixed
   - **Alasan:** Fokus utama saya adalah menciptakan atau mengoptimalkan artefak (algoritma/sistem) untuk memecahkan masalah praktis dan memvalidasinya melalui pengujian teknis.

3. **Identifikasi distorsi:**
   - **Asumsi tersembunyi:** Lingkungan komputasi dianggap selalu stabil dan data input dianggap selalu bersih/valid.
   - **Sumber bias potensial:** Penggunaan data historis yang mungkin tidak lagi relevan dengan kondisi *real-time* saat ini.
   - **Langkah mitigasi:** Melakukan *cross-validation* yang ketat dan menyertakan skenario pengujian dengan data yang memiliki *noise*.

4. **Komitmen etika:**
   - **Data yang tidak akan dimanipulasi:** Hasil mentah (*raw output*) dari eksperimen, meskipun hasilnya tidak mendukung hipotesis awal (hasil negatif).
   - **Batasan yang diakui sejak awal:** Keterbatasan pada spesifikasi perangkat keras dan jangkauan dataset yang digunakan dalam penelitian.

---

##  Latihan 1 — Identifikasi Distorsi

**Paper yang dipilih:**
> **Judul:** Pendekatan Algoritma Genetika Dalam Upaya Optimalisasi Penjadwalan di PT. Nuansa Indah  
> **Penulis (Tahun):** S. Syamsiyah & A. Ma'arif (2022)

| Tahap | Apa yang Dilakukan | Potensi Distorsi |
|-------|-------------------|-----------------|
| **Reality → Data** | Mengambil data urutan produk dan waktu standar mesin dari lantai produksi. | **Inaccuracy Bias:** Waktu standar seringkali berbeda dengan waktu aktual karena faktor kelelahan operator atau gangguan tak terduga. |
| **Data → Processing** | Mengonversi data waktu ke dalam bentuk kromosom dan perhitungan nilai *fitness*. | **Simplification Bias:** Variabel eksternal seperti waktu istirahat atau pergantian shift diabaikan demi penyederhanaan model matematika. |
| **Processing → Analysis** | Menjalankan iterasi algoritma (crossover & mutasi) hingga menemukan nilai *makespan* minimum. | **Local Optima:** Algoritma mungkin terjebak pada solusi "cukup baik" tapi bukan yang terbaik secara global karena parameter mutasi yang kurang dinamis. |
| **Analysis → Inference** | Membandingkan hasil jadwal manual dengan jadwal hasil optimasi Algoritma Genetika. | **Selection Bias:** Ada kemungkinan membandingkan hasil optimasi dengan jadwal manual yang paling buruk, bukan rata-rata kinerja manual. |
| **Inference → Knowledge** | Menyimpulkan bahwa Algoritma Genetika meningkatkan efisiensi waktu sebesar 20,23%. | **Contextual Bias:** Klaim sukses ini dianggap berlaku umum, padahal sangat bergantung pada konfigurasi mesin dan jenis produk saat itu. |

**Distorsi paling besar di tahap:** **Reality → Data**

**Dua distorsi spesifik yang teridentifikasi:**
1. **Measurement Error:** Penggunaan waktu ideal/standar yang tidak mencerminkan fluktuasi produktivitas manusia di lapangan.
2. **Algorithm Bias:** Penentuan nilai parameter genetika (*crossover & mutation rate*) yang dilakukan secara subjektif oleh peneliti (trial-error).

---

##  Latihan 2 — Analisis Kasus Etika

**Skenario:** Peneliti menghapus 3 data point outlier agar hasil menjadi signifikan.

| Perspektif | Analisis |
|------------|---------|
| **Kejujuran ilmiah** | Peneliti harus melaporkan keberadaan outlier tersebut dan menjelaskan mengapa data itu muncul. |
| **Transparansi** | Peneliti wajib menampilkan hasil analisis dengan outlier DAN tanpa outlier agar pembaca bisa menilai secara objektif. |
| **Peer review** | Menyembunyikan outlier adalah bentuk penyesatan informasi yang merusak integritas proses *peer review*. |

**Keputusan akhir dan justifikasi:**
> Tetap menyertakan seluruh data point. Jika outlier dihapus, harus ada alasan teknis yang kuat (misal: kesalahan sensor terbukti) dan hal tersebut harus dideklarasikan secara terbuka dalam laporan riset.

---

##  Latihan 3 — Posisi Paradigma

**Topik riset:** Optimasi Penjadwalan Produksi Menggunakan Algoritma Genetika.

| Kriteria | Positivis | Interpretivis | Design Science |
|----------|-----------|---------------|----------------|
| **Kesesuaian (1–5)** | 4 | 2 | 5 |
| **Jenis data** | Kuantitatif (Waktu, efisiensi, nilai fitness). | Kualitatif (Persepsi operator terhadap jadwal baru). | Pengembangan artefak algoritma dan evaluasi kinerjanya. |
| **Limitasi** | Terlalu kaku pada angka hitungan. | Sangat subjektif dan sulit diukur secara teknis. | Fokus pada "alat" terkadang mengesampingkan teori sosial. |

**Paradigma yang dipilih:** **Design Science** **Alasan:** Riset ini bertujuan untuk memecahkan masalah penjadwalan dengan membangun sebuah instrumen (algoritma) yang kemudian diuji efektivitasnya secara empiris.

---

##  Refleksi

**Jawaban:**
> Sebelum ini, saya cenderung menerima hasil persentase akurasi (seperti 95% atau 20%) sebagai kebenaran mutlak. Setelah memahami rantai distorsi, saya sekarang akan lebih kritis dalam mempertanyakan proses transformasi dari realitas menjadi data. Pertanyaan utama saya kini adalah: **"Apakah data ini benar-benar mewakili realitas, atau hanya mewakili kondisi ideal yang disederhanakan?"**