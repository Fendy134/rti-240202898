# WS-15: Scientific Writing

> **Bab 15 — Penulisan Ilmiah**

---

## Ringkasan Materi

### Scientific Argument Flow

```
Problem → Gap → RQ → Method → Result → Analysis → Conclusion → Contribution
```

Paper ilmiah adalah **satu argumen utuh** dari masalah ke kontribusi. Setiap node harus terhubung logis ke node sebelum dan sesudahnya.

### Struktur IMRAD

| Section | Peran | Pertanyaan Kunci |
|---------|-------|-----------------|
| **Introduction** | Motivasi + frame | Why is this needed? |
| **Method** | Deskripsi (reproducible) | How was it done? |
| **Results** | Laporan objektif | What was found? |
| **Discussion** | Interpretasi + refleksi | What does it mean? |
| **Conclusion** | Ringkasan + kontribusi | So what? |

### Logical Flow — "Red Thread"

Setiap paragraf menjawab satu pertanyaan dan memicu pertanyaan berikutnya. Alur logis ini harus terasa di tiga level:
1. **Antar-kalimat** dalam paragraf
2. **Antar-paragraf** dalam section
3. **Antar-section** dalam paper

### Internal Consistency

Setiap elemen yang dijanjikan di Introduction harus hadir di Discussion/Conclusion.

**Consistency Matrix:**
```
           Intro  Method  Result  Discuss  Conclude
RQ1          ✓      ✓       ✓       ✓        ✓
RQ2          ✓      ✓       ✓       ✗ ←      ✓
Metrik-X     ✗      ✗       ✓ ←     ✗        ✗
```
**Masalah:** RQ2 dibahas di semua bagian kecuali Discussion. Metrik-X muncul di Result tapi tidak diperkenalkan di Method.

### Writing Quality Triad

| Kualitas | Deskripsi | Contoh Buruk → Baik |
|----------|----------|---------------------|
| **Clarity** | Dipahami sekali baca | "Performa meningkat" → "Accuracy meningkat dari 85.3% ke 89.7%" |
| **Precision** | Istilah eksak, tanpa ambiguitas | "signifikan" → "signifikan secara statistik (p=0.003, d=1.2)" |
| **Conciseness** | Setiap kata menambah informasi | Hapus kalimat redundan, filler words |

### Urutan Penulisan yang Disarankan

1. **Method & Results** — paling stabil, tulis pertama
2. **Discussion** — interpretasi berdasarkan hasil
3. **Introduction** — frame sesuai temuan aktual
4. **Abstract & Conclusion** — terakhir

### Target Jumlah Kata

| Section | Target |
|---------|--------|
| Introduction | 500–700 |
| Related Work | 700–1000 |
| Method | 800–1200 |
| Results | 500–800 |
| Discussion | 600–900 |
| Conclusion | 200–400 |

### Jebakan Kognitif

1. "Lebih panjang = lebih lengkap" → conciseness lebih berharga
2. "Introduction harus ditulis pertama" → justru ditulis terakhir
3. "Jargon teknis = lebih ilmiah" → clarity lebih penting
4. "Discussion = ringkasan Results" → Discussion = interpretasi + konteks

---

## Template A.15 — Paper Structure Checklist

```
PAPER STRUCTURE CHECKLIST

Title   : Studi Empiris Komparasi Kinerja ArrayList vs HashMap pada Java 17 LTS Menggunakan JMH
Target  : [x] Jurnal  [ ] Konferensi  [ ] Laporan

Section Check:
  [x] Abstract — masalah, metode, hasil utama, kontribusi (max 250 kata)
  [x] Introduction — konteks → gap → RQ → kontribusi → struktur paper
  [x] Related Work — concept-centric, gap positioning
  [x] Method — reproducible: desain, variabel, metrik, setup, prosedur
  [x] Results — tabel + grafik + observasi (tanpa interpretasi)
  [x] Discussion — interpretasi, perbandingan, implikasi, limitation
  [x] Conclusion — jawaban RQ, kontribusi, future work

Consistency Matrix:
  [x] RQ di Introduction = RQ di Method = RQ di Conclusion
  [x] Variabel di Method = variabel di Results
  [x] Klaim di Discussion didukung data di Results
  [x] Limitasi di Discussion di-address di Conclusion/Future Work

Writing Quality:
  [x] Clarity — mudah dipahami tanpa re-read
  [x] Precision — tidak ada istilah ambigu
  [x] Conciseness — tidak ada kalimat redundan
```

---

## Latihan 1 — Paper Outline

Buat outline paper untuk riset Anda menggunakan struktur IMRAD.

| Section | Konten Utama (2-3 kalimat) | Target Kata |
|---------|---------------------------|------------|
| Abstract | Developer Java memilih struktur data berdasarkan intuisi tanpa panduan empiris. Studi ini membandingkan ArrayList vs HashMap pada 5 operasi CRUD (10³–10⁶ elemen) menggunakan JMH di Java 17 LTS. Hasil: HashMap 94,014x lebih cepat di search, ArrayList 4.6x lebih cepat di iterate. Decision matrix disediakan untuk developer. | 200-250 |
| Introduction | Konteks: Pemilihan struktur data kritis untuk performa Java. Gap: Studi existing menggunakan metodologi lemah (System.currentTimeMillis, single-run, no stats). RQ: Bagaimana perbedaan performa ArrayList vs HashMap pada operasi CRUD dengan JMH + statistical testing? Kontribusi: Benchmark empiris + decision matrix. | 500-700 |
| Related Work | Pujiono et al. (2024): metodologi lemah. Gorelick & Ozsvald (2020): JMH best practice tapi tidak fokus ArrayList vs HashMap. Oracle Docs: theoretical complexity tanpa empirical measurement. Gap: Belum ada JMH + Java 17 LTS + multi-size dataset + statistical testing. | 700-1000 |
| Method | Comparison study: ArrayList vs HashMap, 5 operasi (insert/search/update/delete/iterate), 4 ukuran (10³–10⁶). JMH 1.37: 5 warmup + 10 measurement × 3 forks. Metrik: execution time (ns/op), CI 99.9%. Analisis: pairwise comparison dengan CI overlap test + speedup ratio. | 800-1200 |
| Results | Tabel: mean ± error per operasi × ukuran. HashMap dominan di search (94,014x @ 10⁶), delete (123,313x @ 10⁶), update (9,857x @ 10⁶). ArrayList unggul di iterate (4.6x @ 10³) dan insert (30x @ 10⁵). Decision matrix: 11 HashMap wins, 4 ArrayList wins, 5 TIE. | 500-800 |
| Discussion | Hasil konsisten dengan teori (HashMap O(1), ArrayList O(n)). Boundary condition: iterate @ 10⁶ = TIE (cache miss). Trade-off: HashMap insert @ 10K = 16x slower (rehashing). Limitation: synthetic data, single-threaded. Implikasi: decision matrix untuk production use. | 600-900 |
| Conclusion | RQ terjawab: HashMap dominan di lookup-heavy, ArrayList di iterate-heavy. Kontribusi: (1) Empirical baseline Java 17 LTS, (2) Statistical validation, (3) Decision matrix. Future work: real-world data, concurrent scenario, memory footprint measurement. | 200-400 |

---

## Latihan 2 — Consistency Matrix

Buat consistency matrix untuk memverifikasi internal consistency paper Anda.

|  | Intro | Method | Result | Discussion | Conclusion |
|--|-------|--------|--------|-----------|-----------|
| RQ: Perbedaan performa ArrayList vs HashMap | ✓ | ✓ | ✓ | ✓ | ✓ |
| H1a: HashMap faster di search | ✓ | ✓ | ✓ | ✓ | ✓ |
| H1b: ArrayList faster di iterate | ✓ | ✓ | ✓ | ✓ | ✓ |
| Metrik: execution time (ns/op) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Metrik: CI 99.9% | ✓ | ✓ | ✓ | ✓ | ~ (mention tapi tidak detail) |
| IV: struktur data, operasi, ukuran | ✓ | ✓ | ✓ | ✓ | ✓ |
| DV: execution time, speedup ratio | ✓ | ✓ | ✓ | ✓ | ✓ |
| Kontribusi: decision matrix | ✓ | ~ (implicit) | ✓ | ✓ | ✓ |
| Limitation: synthetic data | ✗ | ✗ | ✗ | ✓ | ✓ |

**Isi setiap sel:** ✓ (ada & konsisten), ✗ (missing), ~ (ada tapi inkonsisten)

**Inkonsistensi yang ditemukan:**
> 1. **CI 99.9%** disebutkan di Intro & Method tapi tidak dijelaskan detail di Conclusion
> 2. **Limitation (synthetic data)** tidak disebutkan di Intro/Method, baru muncul di Discussion
> 3. **Decision matrix** dijanjikan di Intro tapi tidak dijelaskan detail implementasinya di Method

**Tindakan perbaikan:**
> 1. Tambahkan di Conclusion: "All results reported with 99.9% confidence intervals from JMH"
> 2. Tambahkan di Method: "Dataset: synthetic POJO Person with seed=42. Limitation discussed in Section 5."
> 3. Tambahkan di Method: "Decision matrix constructed from pairwise comparison results (Section 4.2)"

---

## Latihan 3 — Writing Quality Check

Ambil satu paragraf dari tulisan Anda (atau tulis paragraf baru) dan evaluasi kualitasnya.

**Paragraf asli:**
> "Hasil penelitian menunjukkan bahwa HashMap lebih cepat dibandingkan ArrayList pada operasi search. Perbedaan performa sangat signifikan terutama pada dataset besar. ArrayList lebih baik untuk operasi iterate karena cache locality."

| Kriteria | Evaluasi | Perbaikan |
|----------|---------|-----------|
| Clarity | ✅ Cukup jelas, tapi "lebih cepat" terlalu umum | Tambahkan angka: "HashMap 94,014x faster" |
| Precision | ❌ "Sangat signifikan" ambigu | Ubah: "statistically significant (CI non-overlapping) with speedup 94,014x" |
| Conciseness | ❌ Kalimat 2 redundan | Hapus kalimat 2, merge info ke kalimat 1 |

**Paragraf setelah perbaikan:**
> "HashMap outperformed ArrayList in search operations with a speedup ratio of 94,014x at 10⁶ elements (p < 0.001, CI non-overlapping). Conversely, ArrayList was 4.6x faster in iterate operations at 10³ elements due to superior cache locality. These findings are statistically significant and practically relevant for production systems."

---

## Refleksi

> Apa perbedaan antara menulis "tentang" riset dan menulis sebagai "argumen" riset? Bagaimana urutan penulisan (Method → Discussion → Introduction) mengubah kualitas tulisan?

> Menulis "tentang" riset cenderung bersifat deskriptif dan kronologis—hanya memaparkan aktivitas yang dilakukan. Sebaliknya, menulis sebagai "argumen" riset berarti membangun narasi logis terpadu (*red thread*) di mana setiap bagian berfungsi untuk membuktikan suatu klaim teoretis atau menjawab *Research Question* (RQ) berdasarkan bukti empiris. Urutan penulisan (Method → Discussion → Introduction) meningkatkan kualitas tulisan secara signifikan karena memaksa peneliti mendasarkan argumen pengantar (*framing*) pada temuan riil yang telah dianalisis. Hal ini mencegah terjadinya *overclaim*, memastikan konsistensi internal antara janji di bagian awal dengan bukti nyata di bagian akhir, serta memfokuskan kontribusi riset secara lebih tajam dan realistis.
