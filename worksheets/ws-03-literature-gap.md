# WS-03: Literature Mapping & Gap

> **Bab 3 — Literature Review, Research Gap & Baseline**

---

## Ringkasan Materi

### Literature Review = Positioning, Bukan Ringkasan

Literature review bukan merangkum paper satu per satu. Pendekatan yang benar adalah **concept-centric** — organisasi berdasarkan tema, metode, atau variabel. Tujuan: menemukan **pola, kontradiksi, dan gap**.

### Empat Jenis Research Gap

| Jenis Gap | Deskripsi | Contoh |
|-----------|----------|--------|
| **Performance Gap** | Performa belum memadai | Akurasi deteksi hanya 78% pada kasus tertentu |
| **Method Gap** | Pendekatan belum diterapkan | Belum ada yang pakai transformer untuk task ini |
| **Data Gap** | Dataset terbatas/tidak representatif | Semua studi pakai dataset sintetis |
| **Context Gap** | Belum diuji pada konteks berbeda | Belum ada evaluasi di negara berkembang |

Gap terkuat = kombinasi 2+ jenis.

### Systematic Search Strategy

1. **Database**: IEEE Xplore, ACM DL, Scopus, Google Scholar
2. **Boolean query** yang terdokumentasi eksplisit
3. **Snowballing**: backward (telusuri referensi) + forward (cari yang mengutip)
4. Klaim "belum ada penelitian" harus didukung **bukti pencarian**

### Baseline Selection — 3 Kriteria

| Kriteria | Pertanyaan |
|----------|-----------|
| **Relevan** | Apakah menyelesaikan masalah yang sama? |
| **Representatif** | Apakah mewakili common practice? |
| **State-of-the-Art** | Apakah terbaru/terbaik? |

Membandingkan deep learning 2024 dengan decision tree sederhana tanpa justifikasi = **straw man comparison** (perbandingan tidak jujur).

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan baca literatur | Mencari solusi yang sudah ada | Memahami apa yang belum terjawab |
| Cara membaca paper | Tutorial, how-to | Metode, limitasi, gap |
| Baseline | Framework terpopuler | State-of-the-art yang rigorous |
| Dokumentasi pencarian | Tidak diperlukan | Wajib (reproducible) |

### Istilah Penting

- **Concept-centric** — Organisasi literatur berdasarkan konsep/metode, bukan per penulis
- **Snowballing** — Backward (telusuri referensi) + Forward (cari yang mengutip paper kunci)
- **Research Position** — Pernyataan eksplisit posisi riset terhadap studi sebelumnya
- **Straw man comparison** — Memilih baseline lemah agar metode sendiri terlihat lebih baik

---

## Template A.3 — Literature Mapping & Gap Identification

```
LITERATURE MAPPING

Topik      : Optimasi Penjadwalan Produksi Menggunakan Algoritma Genetika
Database   : Google Scholar
Query      : "algoritma genetika penjadwalan produksi makespan Indonesia"
Tahun      : 2020–2025
Hasil awal : 30 paper → Screening → 5 paper final

Literature Matrix (concept-centric):

| Study              | Tahun | Method                 | Data                     | Result                                   | Limitation                                      |
|--------------------|-------|------------------------|--------------------------|------------------------------------------|-------------------------------------------------|
| Hatim & Ahmad      | 2022  | GA + SPT + EFT         | Industri manufaktur      | Makespan turun ±20%                      | Hanya fokus makespan, asumsi mesin stabil       |
| Praniasty et al.   | 2024  | GA vs Tabu Search      | Produksi industri        | GA lebih optimal dari metode perusahaan  | Tidak mempertimbangkan energi & availability    |
| Hafiz et al.       | 2023  | Genetic Algorithm      | Penjadwalan mesin        | Optimasi waktu proses                    | Single-objective (makespan saja)                |
| Lestari et al.     | 2023  | Genetic Algorithm      | Penjadwalan perkuliahan  | Mengurangi konflik jadwal                | Model sederhana dan tidak kompleks              |
| Siregar et al.     | 2024  | GA + Neural Network    | Simulasi produksi        | Lebih efisien dari metode konvensional   | Kompleks dan sulit diimplementasikan            |

Pola yang ditemukan:
Metode dominan     : Genetic Algorithm (GA)
Dataset umum       : Produksi industri dan penjadwalan akademik
Limitasi berulang  : Fokus hanya pada makespan, belum mempertimbangkan energi dan availability, asumsi sistem ideal, serta minim perbandingan metode

GAP IDENTIFICATION

Gap 1: [Jenis: performance + method]
Deskripsi    : Sebagian besar penelitian hanya berfokus pada minimasi makespan tanpa mempertimbangkan faktor lain seperti konsumsi energi dan availability mesin.
Bukti        : Hampir seluruh penelitian menggunakan fungsi objektif tunggal berupa waktu penyelesaian produksi.
Signifikansi : Dalam sistem produksi nyata, efisiensi tidak hanya ditentukan oleh waktu tetapi juga oleh penggunaan energi dan keandalan mesin, sehingga pendekatan single-objective menjadi kurang optimal.

Gap 2: [Jenis: context]
Deskripsi    : Model dalam penelitian sebelumnya menggunakan asumsi kondisi ideal seperti mesin selalu tersedia dan tidak ada gangguan produksi.
Bukti        : Sebagian besar penelitian berbasis simulasi atau kondisi stabil tanpa mempertimbangkan ketidakpastian sistem.
Signifikansi : Hal ini menyebabkan hasil penelitian sulit diterapkan secara langsung pada kondisi industri yang dinamis.

Baseline Selection:

| Baseline            | Relevansi                                 | Representatif                          | Source              |
|---------------------|--------------------------------------------|----------------------------------------|---------------------|
| GA + SPT + EFT      | Digunakan pada penjadwalan produksi nyata  | Metode umum pada studi industri        | Hatim & Ahmad, 2022 |
| Genetic Algorithm   | Digunakan pada berbagai kasus scheduling   | Common practice dalam penelitian       | Hafiz et al., 2023  |


Latihan 1 — Concept-Centric Literature Table

Topik riset:
Optimasi Penjadwalan Produksi Menggunakan Algoritma Genetika

Query pencarian:
"algoritma genetika penjadwalan produksi Indonesia"

Database:
Google Scholar

| # | Study            | Tahun | Method       | Dataset    | Result           | Limitasi          |
|---|------------------|-------|-------------|-----------|------------------|-------------------|
| 1 | Hatim & Ahmad    | 2022  | GA + SPT     | Industri  | Makespan turun   | Hanya makespan    |
| 2 | Praniasty et al. | 2024  | GA          | Produksi  | Lebih optimal    | Tidak ada energi  |
| 3 | Hafiz et al.     | 2023  | GA          | Mesin     | Optimasi waktu   | Single-objective  |
| 4 | Lestari et al.   | 2023  | GA          | Kuliah    | Minim konflik    | Sederhana         |
| 5 | Siregar et al.   | 2024  | GA + NN     | Simulasi  | Lebih efisien    | Kompleks          |

Pola yang terlihat — Metode dominan:
Genetic Algorithm (GA)

Limitasi yang berulang:
Fokus pada makespan, tidak mempertimbangkan energi dan availability, serta asumsi sistem ideal


Latihan 2 — Gap Identification

| Jenis Gap        | Ditemukan? | Gap Statement |
|------------------|-----------|---------------|
| Performance Gap  | [✓] Ya    | Optimasi hanya pada makespan tanpa mempertimbangkan efisiensi energi |
| Method Gap       | [✓] Ya    | Belum banyak pendekatan multi-objective sederhana |
| Data Gap         | [ ] Tidak | |
| Context Gap      | [✓] Ya    | Model tidak mencerminkan kondisi nyata (mesin selalu stabil) |

Gap utama yang dipilih:
Multi-objective scheduling (makespan + energi + availability)

Mengapa gap ini penting:
Karena dalam sistem produksi nyata, efisiensi tidak hanya ditentukan oleh waktu penyelesaian tetapi juga oleh konsumsi energi dan keandalan mesin. Pendekatan yang hanya fokus pada makespan tidak cukup untuk menghasilkan solusi yang optimal secara praktis dan aplikatif di industri.


Latihan 3 — Baseline Selection

| # | Baseline                 | Mengapa Relevan                         | Mengapa Representatif              | Apakah SOTA? | Sumber                 |
|---|--------------------------|----------------------------------------|------------------------------------|-------------|------------------------|
| 1 | GA + SPT + EFT          | Sama dengan kasus penjadwalan produksi | Digunakan dalam studi industri     | Tidak       | Hatim & Ahmad, 2022    |
| 2 | Genetic Algorithm       | Digunakan di hampir semua penelitian   | Common practice dalam scheduling   | Tidak       | Hafiz et al., 2023     |

Apakah pemilihan baseline ini bisa dianggap straw man? [ ] Tidak

Justifikasi:
Baseline yang digunakan merupakan metode yang relevan dan umum digunakan dalam penelitian sebelumnya sehingga perbandingan tetap adil dan tidak bias.


Refleksi

Jawaban:
Perbedaan antara klaim “belum ada yang meneliti ini” dengan research gap yang valid terletak pada adanya bukti ilmiah. Research gap yang valid harus didasarkan pada hasil analisis beberapa penelitian sebelumnya yang menunjukkan adanya keterbatasan atau kekurangan yang konsisten.

Cara membuktikan gap adalah dengan melakukan pencarian literatur secara sistematis, kemudian mengidentifikasi pola limitasi yang berulang, seperti metode yang hanya fokus pada satu variabel atau asumsi yang tidak realistis. Dengan demikian, gap yang diambil memiliki dasar yang kuat dan relevan untuk dikembangkan dalam penelitian selanjutnya.