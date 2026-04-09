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
- **Domain:** Manajemen Operasi & Sistem Informasi Manufaktur.
- **Konteks:** Optimasi penjadwalan produksi pada industri furnitur dengan varian produk tinggi.

**System Context**
- **Input:** Daftar 30 jenis produk, estimasi waktu pengerjaan per produk, dan jumlah mesin tersedia.
- **Process:** Penentuan urutan pengerjaan menggunakan mekanisme seleksi, *crossover*, dan mutasi (Algoritma Genetika).
- **Output:** Urutan jadwal produksi baru (Gantt Chart).
- **Outcome:** Reduksi total waktu penyelesaian produksi (*makespan*).
- **Constraints:** Kapasitas mesin tetap, ketergantungan urutan produk, dan parameter algoritma (populasi/generasi).
- **Stakeholders:** Manajer Produksi, Operator Mesin, dan Pemilik PT. Nuansa Indah.

**Fenomena → Problem**
- **Fenomena yang diamati:** Terjadi keterlambatan penyelesaian pesanan dan mesin sering menganggur (*idle*).
- **Gejala (symptom) yang terukur:** Total waktu penyelesaian (*makespan*) mencapai 3.910 menit dengan metode manual.
- **Masalah yang didiagnosis:** Metode *First-Come First-Served* (FCFS) manual tidak mampu menangani kombinasi urutan produk yang kompleks secara efisien.
- **Masalah riset (researchable):** Sejauh mana implementasi Algoritma Genetika dapat meminimalkan *makespan* dibandingkan metode konvensional pada kasus penjadwalan 30 produk?
- **Variabel yang terukur:** Nilai *Fitness*, Durasi *Makespan* (Menit), dan Persentase Peningkatan Efisiensi (%).

**Problem Quality Check**
- [X] **Clarity** — Masalah spesifik pada inefisiensi jadwal.
- [X] **Measurability** — Menggunakan metrik waktu (menit) yang absolut.
- [X] **Relevance** — Berkontribusi pada efisiensi operasional industri.
- [X] **Testability** — Dapat dibandingkan langsung antara hasil manual vs algoritma.
- [X] **Impact** — Mempercepat waktu produksi dan mengurangi biaya operasional.

**Problem Statement (1 Paragraf):**
PT. Nuansa Indah menghadapi kendala inefisiensi produksi di mana metode penjadwalan manual mengakibatkan *makespan* yang tinggi sebesar 3.910 menit. Hal ini disebabkan oleh ketidakmampuan metode konvensional dalam mengoptimalkan urutan pengerjaan 30 jenis produk pada sumber daya yang terbatas. Penelitian ini bertujuan untuk menguji efektivitas Algoritma Genetika dalam mereduksi waktu produksi melalui pencarian solusi urutan global yang optimal, guna menghasilkan sistem penjadwalan yang lebih presisi dan efisien.

---

##  Latihan 1 — Dari Topik ke Masalah Riset

**Topik awal:** Optimasi Penjadwalan Produksi Industri.

| Tahap | Hasil |
|-------|-------|
| **Reality** | Pabrik sering mengalami lembur akibat jadwal produksi yang tidak teratur. |
| **Observed Issue (Symptom)** | *Makespan* produksi mencapai 3.910 menit dan terjadi penumpukan barang. |
| **Diagnosed Problem (Root Cause)** | Penggunaan metode urutan manual (FCFS) yang tidak mempertimbangkan variansi waktu pengerjaan antar produk. |
| **Researchable Problem** | Analisis perbandingan performa antara metode manual dan Algoritma Genetika dalam minimasi *makespan*. |
| **Measurable Variable** | Total durasi waktu produksi (*makespan*) dalam satuan menit. |

**Apakah terjebak solution-first thinking?** [ ] Ya / [X] Tidak  
> **Justifikasi:** Analisis dimulai dari masalah nyata (keterlambatan produksi), bukan sekadar ingin menggunakan algoritma tanpa urgensi masalah.

---

##  Latihan 2 — System Context Decomposition

| Komponen | Deskripsi |
|----------|----------|
| **Input** | Data 30 item produk dan matriks waktu pengerjaan masing-masing mesin. |
| **Process** | Pencarian kombinasi urutan terbaik melalui iterasi evolusi Algoritma Genetika. |
| **Output** | Urutan pengerjaan (*job sequence*) yang memiliki total waktu terkecil. |
| **Outcome** | Efisiensi waktu produksi sebesar 20,23% (dari 3.910 ke 3.119 menit). |
| **Constraints** | Jumlah mesin yang statis dan parameter probabilitas mutasi/crossover. |
| **Stakeholders** | Tim produksi yang membutuhkan kepastian jadwal pengerjaan. |

**Komponen mana yang paling relevan dengan masalah riset?** **Process** (Karena efektivitas pencarian urutan sangat bergantung pada algoritma yang digunakan).

---

##  Latihan 3 — Problem Quality Check

| Kriteria | Skor (1-5) | Justifikasi |
|----------|-----------|-------------|
| **Clarity** | 5 | Fokus pada satu masalah: optimasi durasi waktu penjadwalan. |
| **Measurability** | 5 | Hasil diukur dengan perbandingan waktu menit yang sangat kontras. |
| **Relevance** | 4 | Sangat berguna untuk industri manufaktur serupa. |
| **Testability** | 5 | Hipotesis bahwa AG lebih baik dari manual sangat mudah diuji melalui simulasi. |
| **Impact** | 4 | Memberikan efisiensi nyata pada manajemen waktu perusahaan. |

**Skor total:** **23 / 25**

**Problem statement versi final (1 paragraf):** Inefisiensi penjadwalan manual di PT. Nuansa Indah menyebabkan durasi produksi yang tidak optimal, mencapai 3.910 menit untuk satu siklus pengerjaan. Masalah ini berakar pada penggunaan metode urutan sederhana yang tidak mampu mengelola kompleksitas 30 varian produk secara efisien. Melalui pendekatan *Design Science*, riset ini mengimplementasikan Algoritma Genetika untuk menemukan urutan produksi optimal yang dapat meminimalkan waktu *idle* mesin, dengan target peningkatan efisiensi yang terukur secara kuantitatif melalui durasi *makespan*.

---

##  Refleksi

**Jawaban:** Perbedaan fundamentalnya terletak pada **sifat solusinya**. Masalah coding (bug/error) bersifat reaktif dan tujuannya adalah perbaikan teknis agar sistem kembali berfungsi (*corrective*). Sedangkan masalah riset bersifat proaktif dan bertujuan untuk membuktikan sebuah klaim atau mencari pengetahuan baru (*explorative*). Dalam riset, "masalah" bukan sekadar error, melainkan sebuah tantangan untuk membuktikan bahwa ada cara yang lebih baik, lebih cepat, atau lebih efisien berdasarkan data yang dapat direplikasi oleh orang lain.