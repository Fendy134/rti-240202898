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
|-------|------|-----------|
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

## Template A.4 — RQ-Contribution-Hypothesis

```
RQ-CONTRIBUTION-HYPOTHESIS

Gap Statement  : Sebagian besar penelitian hanya mengoptimalkan makespan tanpa mempertimbangkan energi dan availability mesin. Model penelitian masih menggunakan asumsi kondisi ideal (mesin selalu tersedia, tanpa gangguan).

Research Question:
  Tipe         : [X] Comparison  [ ] Improvement  [ ] Exploratory
  Formulasi    : Apakah Algoritma Genetika multi-objective menghasilkan solusi penjadwalan yang lebih optimal (makespan lebih rendah, energi lebih efisien, availability lebih tinggi) dibandingkan dengan GA single-objective dan metode manual pada kasus penjadwalan 30 produk di PT. Nuansa Indah?
  Variabel IV  : Metode penjadwalan (GA multi-objective, GA single-objective, Manual FCFS)
  Variabel DV  : Makespan (menit), Konsumsi energi (kWh), Availability mesin (%)
  Metrik       : Durasi makespan, Total energi, Persentase availability, Persentase peningkatan efisiensi
  Dataset      : Data historis PT. Nuansa Indah (30 produk, 5 mesin, waktu standar per produk per mesin)
  Baseline     : GA single-objective (hanya makespan) dan metode manual FCFS

Quality Check RQ:
  [X] Variabel spesifik
  [X] Metrik jelas
  [X] Baseline ada
  [X] Konteks disebutkan
  [X] Memerlukan eksperimen (bukan hanya survei literatur)

Contribution Statement:
  Apa yang baru diketahui : Efektivitas GA multi-objective dalam mengoptimalkan penjadwalan produksi dengan mempertimbangkan trade-off antara makespan, energi, dan availability secara simultan, serta perbandingan sistematis dengan GA single-objective dan metode manual
  Jenis kontribusi        : [X] Improvement  [X] Comparison  [ ] Novel approach
  Gap yang diisi          : Mengisi gap penelitian tentang optimasi multi-objective pada penjadwalan produksi yang belum banyak diteliti, terutama dalam konteks industri manufaktur dengan kondisi real-time

Hypothesis Pair:
  H₀ : Tidak ada perbedaan signifikan dalam performa penjadwalan (makespan, energi, availability) antara GA multi-objective, GA single-objective, dan metode manual pada kasus penjadwalan 30 produk di PT. Nuansa Indah
  H₁ : GA multi-objective menghasilkan performa penjadwalan yang signifikan lebih baik (makespan lebih rendah, energi lebih efisien, availability lebih tinggi) dibandingkan GA single-objective dan metode manual
  Threshold              : Perbedaan makespan ≥ 15%, efisiensi energi ≥ 10%, availability ≥ 5% dengan p-value < 0.05
  Justifikasi threshold  : Berdasarkan studi sebelumnya (Hatim & Ahmad 2022), GA mampu mengurangi makespan ±20%. Threshold 15% dianggap signifikan secara praktis untuk industri. Energi dan availability ditetapkan lebih konservatif karena belum banyak baseline yang tersedia. P-value < 0.05 adalah standar signifikansi statistik dalam penelitian
```

---

## Latihan 1 — Dari Gap ke RQ

Gunakan gap yang ditemukan di WS-03. Transformasikan menjadi Research Question.

**Gap dari WS-03:** Sebagian besar penelitian hanya mengoptimalkan makespan tanpa mempertimbangkan faktor lain seperti konsumsi energi dan availability mesin. Model penelitian masih menggunakan asumsi kondisi ideal (mesin selalu tersedia, tanpa gangguan).

**RQ versi pertama (tulis bebas):**
> Apakah Algoritma Genetika dapat mengoptimalkan penjadwalan produksi dengan mempertimbangkan multiple objectives (makespan, energi, dan availability)?

**Evaluasi RQ:**

| Komponen | Ada? | Isi |
|----------|------|-----|
| Metode spesifik | Ya | Algoritma Genetika dengan multi-objective optimization |
| Metrik terukur | Ya | Makespan (menit), Konsumsi energi (kWh), Availability (%) |
| Baseline | Tidak | Perlu ditambahkan: GA single-objective atau metode konvensional |
| Dataset/konteks | Ya | Industri furnitur dengan 30 produk dan kondisi real-time |

**Tipe RQ:** [X] Comparison / [ ] Improvement / [ ] Exploratory

**RQ versi revisi (setelah evaluasi):**
> Apakah Algoritma Genetika multi-objective menghasilkan solusi penjadwalan yang lebih optimal (makespan lebih rendah, energi lebih efisien, availability lebih tinggi) dibandingkan dengan GA single-objective dan metode manual pada kasus penjadwalan 30 produk di PT. Nuansa Indah?

---

## Latihan 2 — Hypothesis Pair

Rumuskan pasangan hipotesis dari RQ di Latihan 1.

| Komponen | Isi |
|----------|-----|
| H₀ | Tidak ada perbedaan signifikan dalam performa penjadwalan (makespan, energi, availability) antara GA multi-objective, GA single-objective, dan metode manual pada kasus penjadwalan 30 produk di PT. Nuansa Indah |
| H₁ | GA multi-objective menghasilkan performa penjadwalan yang signifikan lebih baik (makespan lebih rendah, energi lebih efisien, availability lebih tinggi) dibandingkan GA single-objective dan metode manual |
| Metrik | Makespan (menit), Konsumsi energi (kWh), Availability (%) |
| Threshold | Perbedaan makespan ≥ 15%, efisiensi energi ≥ 10%, availability ≥ 5% dengan p-value < 0.05 |
| Justifikasi threshold | Berdasarkan studi sebelumnya (Hatim & Ahmad 2022), GA mampu mengurangi makespan ±20%. Threshold 15% dianggap signifikan secara praktis untuk industri. Energi dan availability ditetapkan lebih konservatif karena belum banyak baseline yang tersedia |

**Apakah hipotesis ini falsifiable?** [X] Ya / [ ] Tidak
> Bagaimana cara membuktikannya salah? Jika hasil eksperimen menunjukkan p-value > 0.05 atau perbedaan performa di bawah threshold yang ditetapkan, maka H₀ tidak ditolak dan H₁ ditolak. Dengan demikian, klaim bahwa GA multi-objective lebih baik tidak terbukti secara statistik.

---

## Latihan 3 — Rantai Operasionalisasi

Lengkapi rantai dari RQ hingga metode analisis.

| Tahap | Isi |
|-------|-----|
| RQ | Apakah GA multi-objective menghasilkan solusi penjadwalan lebih optimal (makespan, energi, availability) dibanding GA single-objective dan metode manual? |
| Variable (IV) | Jenis metode penjadwalan: (1) GA multi-objective, (2) GA single-objective, (3) Metode manual FCFS |
| Variable (DV) | Performa penjadwalan: makespan, konsumsi energi, availability mesin |
| Metric | Makespan (menit), Energi (kWh), Availability (%) |
| Data source | Simulasi produksi dengan data historis PT. Nuansa Indah (30 produk, 5 mesin) |
| Analysis method | ANOVA one-way untuk perbandingan 3 grup, post-hoc Tukey HSD, effect size (Cohen's d) |

**Apakah rantai lengkap?** [X] Ya / [ ] Tidak
> Jika tidak, tahap mana yang perlu direvisi? Rantai sudah lengkap dari RQ hingga metode analisis. Setiap tahap terhubung logis tanpa lompatan.

---

## Refleksi

> Ambil satu judul skripsi/paper yang pernah dibaca. Coba ekstrak RQ-nya. Apakah RQ tersebut memenuhi semua komponen (metode, metrik, baseline, konteks)? Jika tidak, apa yang hilang?

**Judul:** Pendekatan Algoritma Genetika Dalam Upaya Optimalisasi Penjadwalan di PT. Nuansa Indah (Syamsiyah & Ma'arif, 2022)

**RQ yang diekstrak:** Apakah Algoritma Genetika dapat mengoptimalkan penjadwalan produksi dengan mengurangi makespan dibandingkan metode manual?

**Komponen yang hilang:** 
- Metrik terukur tidak spesifik (hanya "makespan" tanpa satuan atau threshold)
- Baseline tidak jelas (metode manual apa? FCFS? Prioritas?)
- Konteks terbatas (tidak menyebutkan jumlah produk, mesin, atau karakteristik industri secara detail)
- Tidak ada secondary metric (hanya fokus makespan, tidak mempertimbangkan energi atau availability)

**Kesimpulan:** RQ dalam paper tersebut masih terlalu umum dan perlu diperkuat dengan spesifikasi metrik, baseline yang jelas, dan konteks yang lebih detail agar menjadi research question yang matang dan testable.
