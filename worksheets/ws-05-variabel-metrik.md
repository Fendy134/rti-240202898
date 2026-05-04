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
| **Ratio** | Jarak bermakna + nol absolut | Waktu eksekusi (ms) | Semua operasi |

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
|-------|------------|----------|
| Pemilihan metrik | Berdasarkan kebiasaan/tool yang ada | Berdasarkan construct validity |
| Anomali | Dihapus untuk laporan bersih | Diinvestigasi — bisa jadi temuan |
| Kapan dipilih | Setelah sistem jadi (monitoring) | Sebelum eksperimen (by design) |

### Istilah Penting

- **Operationalization** — Transformasi konsep abstrak menjadi variabel terukur
- **Construct Validity** — Sejauh mana pengukuran benar-benar mengukur konsep yang dimaksud
- **Measurement Scale** — Klasifikasi data (NOIR) yang menentukan analisis valid
- **Multi-metric Evaluation** — Menggunakan beberapa metrik untuk menangkap konsep kompleks

---

## Template A.5 — Definisi Variabel, Metrik & Justifikasi

```
VARIABLE & METRIC DEFINITION

Research Question: Apakah GA multi-objective menghasilkan solusi penjadwalan lebih optimal (makespan, energi, availability) dibanding GA single-objective dan metode manual pada kasus penjadwalan 30 produk di PT. Nuansa Indah?

| Variabel | Tipe | Konsep | Metrik | Skala | Satuan | Cara Mengukur | Justifikasi |
|----------|------|--------|--------|-------|--------|---------------|-------------|
| Metode penjadwalan | IV | Pendekatan optimasi yang digunakan | Kategori: GA multi-obj, GA single-obj, Manual FCFS | Nominal | — | Konfigurasi parameter algoritma di config file | Variabel independen yang dimanipulasi untuk membandingkan performa |
| Makespan | DV | Total waktu penyelesaian semua produk | Durasi dari job pertama hingga job terakhir selesai | Ratio | Menit | Logger otomatis mencatat timestamp start/end setiap job | Primary metric yang langsung terikat hipotesis; representatif untuk efisiensi waktu |
| Konsumsi energi | DV | Efisiensi penggunaan daya mesin | Total energi yang dikonsumsi selama proses produksi | Ratio | kWh | Energy tracker mengakumulasi daya per mesin per unit waktu | Primary metric untuk mengukur efisiensi energi; feasible dari simulasi |
| Availability mesin | DV | Keandalan mesin dalam operasi | Persentase waktu mesin aktif vs total waktu tersedia | Ratio | % | Availability monitor menghitung (uptime / total_time) × 100 | Primary metric untuk mengukur keandalan; sensitive terhadap downtime |
| Jumlah produk | CV | Kompleksitas penjadwalan | Jumlah job yang dijadwalkan | Ratio | Unit | Dikunci di config file: num_jobs = 30 | Control variable untuk memastikan semua eksperimen menggunakan dataset yang sama |
| Jumlah mesin | CV | Kapasitas sumber daya | Jumlah mesin yang tersedia | Ratio | Unit | Dikunci di config file: num_machines = 5 | Control variable untuk memastikan kapasitas sumber daya konsisten |
| Parameter GA | CV | Konfigurasi algoritma genetika | Population size, generations, mutation rate, crossover rate | Ratio | — | Dikunci di config file untuk semua metode GA | Control variable untuk memastikan fair comparison antar metode GA |

Alignment Check:
  RQ → Concept → Variable → Metric → Data → Result
  [X] Setiap langkah terdokumentasi
  [X] Tidak ada "lompatan logis"
  [X] Metrik mengukur apa yang dimaksud (construct validity)
```

---

## Latihan 1 — Operationalization Chain

Gunakan RQ dari WS-04. Definisikan variabel dan metriknya.

**RQ:** Apakah GA multi-objective menghasilkan solusi penjadwalan lebih optimal (makespan, energi, availability) dibanding GA single-objective dan metode manual?

| Variabel | Tipe | Konsep Abstrak | Metrik Konkret | Skala (NOIR) | Satuan |
|----------|------|---------------|----------------|-------------|--------|
| Metode penjadwalan | IV | Pendekatan optimasi yang digunakan | Kategori: GA multi-obj, GA single-obj, Manual FCFS | Nominal | — |
| Makespan | DV | Total waktu penyelesaian semua produk | Durasi dari job pertama hingga job terakhir selesai | Ratio | Menit |
| Konsumsi energi | DV | Efisiensi penggunaan daya mesin | Total energi yang dikonsumsi selama proses produksi | Ratio | kWh |
| Availability mesin | DV | Keandalan mesin dalam operasi | Persentase waktu mesin aktif vs total waktu tersedia | Ratio | % |
| Jumlah produk | CV | Kompleksitas penjadwalan | Jumlah job yang dijadwalkan | Ratio | Unit |
| Jumlah mesin | CV | Kapasitas sumber daya | Jumlah mesin yang tersedia | Ratio | Unit |

**Apakah ada lompatan logis dalam rantai?** [ ] Ya / [X] Tidak
> Jika ya, di mana? Rantai sudah lengkap dan logis. Setiap konsep abstrak diterjemahkan menjadi metrik konkret dengan skala dan satuan yang jelas.

---

## Latihan 2 — Evaluasi Metrik

Evaluasi metrik DV yang dipilih di Latihan 1 menggunakan 3 kriteria.

| Kriteria | Skor (1-5) | Justifikasi |
|----------|-----------|-------------|
| Representative | 5 | Makespan, energi, dan availability secara langsung mewakili efisiensi penjadwalan yang diinginkan dalam industri manufaktur |
| Sensitive | 4 | Ketiga metrik cukup peka menangkap perbedaan performa antar metode. Makespan sangat sensitif terhadap urutan job; energi sensitif terhadap idle time mesin; availability sensitif terhadap downtime |
| Feasible | 5 | Semua metrik dapat dikumpulkan dari simulasi atau data historis perusahaan tanpa biaya tambahan yang signifikan |

**Apakah perlu secondary metric?** [X] Ya / [ ] Tidak
> Jika ya, apa dan mengapa? Secondary metric yang perlu ditambahkan: (1) **Utilization Rate** — mengukur seberapa efisien mesin digunakan (menghindari idle time), (2) **Robustness** — mengukur stabilitas solusi terhadap variasi input (noise), (3) **Computational Time** — mengukur waktu eksekusi algoritma untuk mengevaluasi trade-off antara kualitas solusi dan kecepatan komputasi. Ketiga secondary metric ini memberikan gambaran lebih lengkap tentang performa praktis dari setiap metode.

**Contoh kasus ceiling effect untuk metrik ini:**
> Ceiling effect bisa terjadi pada metrik Availability jika semua metode mencapai 95%+ availability. Dalam kasus ini, metrik tidak lagi sensitif membedakan performa antar metode. Untuk mengatasi ini, bisa ditambahkan metrik yang lebih granular seperti "Mean Time Between Failures (MTBF)" atau "Downtime frequency" yang lebih peka terhadap perbedaan kecil dalam keandalan mesin.

---

## Latihan 3 — Data Quality Check

Bayangkan data yang akan dikumpulkan dari eksperimen. Evaluasi 4 dimensi kualitas data.

| Dimensi | Pertanyaan | Jawaban | Strategi Mitigasi |
|---------|-----------|---------|------------------|
| Completeness | Apakah semua data point terkumpul? | Sebagian besar data akan terkumpul dari simulasi, namun ada risiko data historis perusahaan tidak lengkap untuk semua 30 produk | Melakukan data cleaning dan imputation untuk missing values; menggunakan data sintetis yang realistis untuk melengkapi gap |
| Consistency | Apakah ada kontradiksi internal? | Ada potensi inkonsistensi antara waktu standar mesin vs waktu aktual; satuan energi mungkin berbeda antar mesin | Melakukan normalisasi data; mendokumentasikan asumsi konversi satuan; melakukan validasi silang dengan tim produksi |
| Validity | Apakah benar-benar mengukur yang dimaksud? | Makespan valid mengukur durasi; energi valid jika menggunakan meter yang terkalibrasi; availability valid jika mencatat downtime dengan akurat | Melakukan pre-test dengan data sampel; melakukan audit terhadap sumber data; melibatkan domain expert untuk validasi |
| Representativeness | Apakah sampel mewakili populasi target? | Data dari PT. Nuansa Indah mungkin tidak mewakili semua industri furnitur; kondisi ideal simulasi mungkin tidak mencerminkan realitas lapangan | Melakukan sensitivity analysis dengan variasi parameter; melakukan cross-validation dengan data dari perusahaan lain jika memungkinkan; mendokumentasikan batasan generalisasi |

---

## Refleksi

> Mengapa memilih metrik setelah melihat data dianggap p-hacking? Apa bedanya dengan eksplorasi data yang sah?

**Jawaban:**
> **P-hacking** adalah praktik memilih metrik atau analisis statistik setelah melihat hasil data dengan tujuan untuk mendapatkan p-value < 0.05 agar hipotesis terlihat signifikan. Ini melanggar prinsip falsifiability karena peneliti secara implisit "menyesuaikan" pertanyaan dengan jawaban yang sudah ada.
>
> **Perbedaan dengan eksplorasi data yang sah:**
> - **P-hacking**: Metrik dipilih SETELAH melihat data dengan tujuan menemukan signifikansi (confirmatory bias)
> - **Eksplorasi sah**: Metrik tambahan ditemukan SETELAH analisis utama selesai, dilaporkan sebagai "exploratory findings" (bukan confirmatory), dan dinyatakan dengan jelas bahwa ini adalah post-hoc analysis yang memerlukan validasi lebih lanjut
>
> **Strategi untuk menghindari p-hacking:**
> 1. **Pre-registration**: Tentukan metrik dan analisis SEBELUM eksperimen dimulai
> 2. **Primary vs Secondary**: Pisahkan metrik utama (untuk menjawab hipotesis) dari metrik tambahan (untuk eksplorasi)
> 3. **Transparansi**: Laporkan semua analisis yang dilakukan, bukan hanya yang signifikan
> 4. **Bonferroni correction**: Jika melakukan multiple testing, gunakan koreksi statistik untuk mengurangi false positive rate
