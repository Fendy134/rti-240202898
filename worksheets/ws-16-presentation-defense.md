# WS-16: Presentation & Defense (UAS)

> **Bab 16 — Presentasi & Pertahanan Ilmiah**

---

## Ringkasan Materi

### Scientific Defense Model

```
Research Work → Presentation → Questioning → Defense → Evaluation → Acceptance
```

### Presentasi ≠ Ringkasan Paper

| Paper | Presentasi |
|-------|-----------|
| Dibaca (self-paced) | Didengar (presenter-paced) |
| Detail lengkap | Ide kunci + highlight |
| Tabel numerik detail | Grafik visual + angka kunci |
| Pembaca bisa re-read | Audiens dengar sekali |

**Prinsip:** Presentasi membutuhkan **reformulasi**, bukan kompresi. Medium berbeda = pendekatan berbeda.

### Claim-Evidence-Reasoning (CER)

Setiap jawaban defense harus memiliki:
1. **Claim** — Pernyataan yang dijawab
2. **Evidence** — Data/fakta pendukung
3. **Reasoning** — Logika yang menghubungkan evidence ke claim

**Contoh:**
| Pertanyaan | Bad Answer | Good Answer (CER) |
|-----------|-----------|-------------------|
| "Kenapa hanya 3 dataset?" | "Tiga sudah cukup" | "3 dataset mewakili variasi: small-clean, medium-clean, medium-noisy [E]. Generalisasi perlu validasi lanjut — listed as limitation [R]" |
| "Hasil DS-3 menurun?" | "Itu outlier" | "Ya, karena distribusi heavy-tail melanggar asumsi Gaussian [E]. Ini menunjukkan boundary condition metode [R]" |
| "Effect size?" | "p=0.003, jadi signifikan" | "Cohen's d=1.2 (large effect) [E] — bukan hanya signifikan tapi substansial [R]" |

### Slide Design — One Slide, One Message

**Optimal 9-Slide Plan (15 menit):**

| # | Slide | Waktu | Pesan |
|---|-------|-------|-------|
| 1 | Title + context | 1 min | Apa ini tentang apa |
| 2 | Problem + motivation | 2 min | Mengapa penting |
| 3 | Gap + RQ | 1.5 min | Apa yang belum terjawab |
| 4 | Method overview | 2 min | Bagaimana dijawab (diagram) |
| 5 | Key result — tabel | 2 min | Temuan utama |
| 6 | Key result — grafik | 2 min | Pola visual |
| 7 | Interpretation + failure | 2 min | Apa artinya |
| 8 | Limitation + future | 1.5 min | Batasan & arah |
| 9 | Conclusion + contribution | 1 min | Closing message |

### Anticipatory Defense

Prediksi pertanyaan berdasarkan kategori:

| Kategori | Contoh Pertanyaan |
|---------|------------------|
| Problem | "Mengapa masalah ini penting?" |
| Gap | "Bagaimana dengan studi X yang sudah menjawab ini?" |
| Method | "Mengapa metode ini, bukan Y?" |
| Results | "Bagaimana menjelaskan anomali di DS-3?" |
| Generalization | "Apakah bisa diterapkan di domain lain?" |

### Tiga Prinsip Jawaban

1. **Direct** — Jawab dulu, elaborasi kemudian
2. **Data-based** — Tunjuk evidence spesifik
3. **Honest** — Akui limitasi jika memang ada

### Jebakan Kognitif

1. "Presentasi = semua yang ada di paper" → terlalu padat
2. "Slide cantik = presentasi bagus" → konten > estetika
3. "Tidak bisa jawab = gagal" → "I don't know, but..." menunjukkan kejujuran
4. "Tidak perlu latihan — saya paham riset saya" → latihan = menemukan celah

---

## Template A.16 — Defense Preparation Sheet

```
DEFENSE PREPARATION

Slide Deck Plan:
  Total slides   : 10 slides (target: 10-12 konten + title/closing)
  Time per slide : ~2 min
  Total time     : 15 menit

Slide Outline:
| # | Pesan Utama | Visual | Waktu |
|---|-------------|--------|-------|
| 1 | Title & Context | Title slide | 1 min |
| 2 | Problem & Motivation | Diagram trade-off performa | 1.5 min |
| 3 | Gap & RQ | Tabel komparasi penelitian terdahulu | 1.5 min |
| 4 | Method Overview | Diagram alur komparasi & setup JMH/JOL | 2 min |
| 5 | Key Result: Execution Time | Heatmap & Speedup plots | 2.5 min |
| 6 | Key Result: Memory Footprint | Bar chart bytes/element | 2 min |
| 7 | Interpretation & Decision Matrix | Heatmap Matrix & boundary conditions | 2 min |
| 8 | Limitations & Future Work | Bullet points list | 1 min |
| 9 | Conclusion & Contribution | Summary bullet points | 1.5 min |

Anticipatory Defense Matrix:
| Kategori | Pertanyaan Potensial | Jawaban (CER) |
|----------|---------------------|---------------|
| Problem  | Mengapa membandingkan ArrayList dan HashMap yang teoretis sudah jelas beda? | Teoretis (Big-O) tidak mencerminkan overhead runtime riil JVM modern seperti JIT compiler, GC, dan cache locality. |
| Gap      | Apa bedanya dengan benchmark yang sudah ada? | Penelitian terdahulu menggunakan metodologi lemah (System.currentTimeMillis) dan tanpa uji statistik formal (ANOVA/Tukey HSD). |
| Method   | Mengapa menggunakan JMH, bukan manual timer? | JMH mengisolasi GC overhead dan warm-up JVM secara otomatis, menjamin pengukuran mikrobenchmark akurat. |
| Results  | Mengapa ArrayList.iterate setara HashMap pada 1M? | Terjadi cache miss L1/L2 pada ArrayList akibat ukuran dataset yang terlampau besar, meniadakan keuntungan cache locality. |
| Generalization | Apakah berlaku di concurrent scenario? | Tidak secara langsung. Untuk multithreading diperlukan sinkronisasi eksternal atau concurrent classes (ConcurrentHashMap). |

Latihan:
  Latihan 1: 2026-05-18 — Timing 16 menit, feedback: kurangi detail slide metodologi
  Latihan 2: 2026-05-19 — Timing 14 menit, feedback: intonasi saat transisi hasil memori diperbaiki
  Latihan 3: 2026-05-19 — Timing 15 menit, feedback: simulasi Q&A berjalan lancar, siap UAS
```

---

## Latihan 1 — Slide Outline

Rencanakan presentasi 15 menit untuk riset Anda.

| # | Pesan Utama | Visual yang Digunakan | Waktu |
|---|-------------|----------------------|-------|
| 1 | Judul & Konteks: Komparasi ArrayList vs HashMap pada Java 17 LTS | Title slide | 1 min |
| 2 | Problem: Pemilihan struktur data Java sering didasarkan pada intuisi tanpa baseline empiris komprehensif | Diagram trade-off performa | 1.5 min |
| 3 | Gap & RQ: Kurangnya benchmark terstandar menggunakan JMH dan pengujian statistik inferensial (ANOVA & Tukey HSD) | Tabel komparasi penelitian terdahulu | 1.5 min |
| 4 | Metode Riset: Setup JMH (5 warmup, 10 measurement, 3 forks), parameter dataset 10³–10⁶, dan JOL Memory Profiler | Diagram alur metodologi | 2 min |
| 5 | Hasil 1: Performa Waktu Eksekusi | Heatmap Waktu Eksekusi (fig_execution_time.png) & Speedup Ratio (fig_speedup_ratio.png) | 2.5 min |
| 6 | Hasil 2: Penggunaan Memori (Memory Footprint) | Grafik total deep size & bytes/element (fig_memory_footprint.png) | 2 min |
| 7 | Interpretasi & Decision Matrix | Heatmap rekomendasi data structure (fig_decision_matrix.png) & boundary conditions | 2 min |
| 8 | Keterbatasan (Limitation) | Analisis keterbatasan (synthetic data, single-threaded) & rencana mitigasi | 1 min |
| 9 | Kesimpulan & Kontribusi | Ringkasan jawaban RQ, baseline empiris baru, dan closing message | 1.5 min |

**Total waktu estimasi:** 15 menit

---

## Latihan 2 — Anticipatory Defense

Prediksi 5 pertanyaan yang mungkin diajukan penguji, lalu siapkan jawaban CER.

| # | Kategori | Pertanyaan | Claim | Evidence | Reasoning |
|---|----------|-----------|-------|----------|-----------|
| 1 | Problem | Mengapa membandingkan ArrayList dan HashMap yang secara teoretis sudah jelas memiliki perbedaan kompleksitas waktu? | Kompleksitas teoretis (Big-O) tidak selalu mencerminkan performa nyata di runtime JVM modern karena adanya optimasi seperti JIT compiler, garbage collection, dan cache locality. | Hasil benchmark menunjukkan operations/ns bervariasi bergantung pada ukuran dataset dan JVM warm-up. | Evaluasi empiris diperlukan untuk mengetahui overhead riil dan memetakan boundary conditions praktis bagi developer. |
| 2 | Method | Mengapa menggunakan framework JMH, bukan pengukuran manual System.currentTimeMillis() atau System.nanoTime()? | Pengukuran manual sangat rentan terhadap distorsi runtime seperti warm-up JVM, dead-code elimination, dan garbage collection overhead. | Dokumentasi JMH (Oracle) dan hasil benchmark yang stabil tanpa deviasi ekstrem. | JMH mengisolasi variabel pengganggu tersebut melalui iterasi warm-up dan Blackhole consumption untuk menjamin akurasi mikrobenchmark. |
| 3 | Method | Mengapa Anda mengukur memori menggunakan Java Object Layout (JOL) dan bukan Runtime.getRuntime().freeMemory()? | JOL memberikan visualisasi footprint memori objek secara presisi di heap memory, terbebas dari overhead Garbage Collector (GC). | memory_footprint.csv menunjukkan shallow size dan deep size yang konsisten untuk setiap ukuran dataset. | freeMemory() mengukur heap secara keseluruhan yang dipengaruhi oleh aktivitas thread lain dan waktu eksekusi GC, sehingga tidak akurat untuk objek individu. |
| 4 | Results | Mengapa HashMap.insert lebih lambat secara signifikan dibandingkan ArrayList.insert pada dataset kecil (1K elemen)? | HashMap memiliki overhead struktural yang besar karena alokasi node entry dan penghitungan hash index, sedangkan ArrayList hanya melakukan array append (O(1)). | ArrayList.insert (20.8 ns) vs HashMap.insert (537.9 ns) pada 1K elemen. | Overhead struktural HashMap mendominasi eksekusi pada ukuran kecil, membuat ArrayList jauh lebih efisien untuk operasi penambahan sederhana. |
| 5 | Generalization | Apakah hasil benchmark ini dapat digeneralisasikan untuk skenario multithreading (concurrency)? | Tidak secara langsung, karena ArrayList dan HashMap tidak thread-safe secara bawaan. | Dokumentasi Java API menyatakan kedua kelas tersebut tidak aman untuk diakses konkuren tanpa sinkronisasi eksternal. | Untuk skenario multithreaded, performa akan dipengaruhi oleh locking overhead, sehingga memerlukan pengujian terpisah pada ConcurrentHashMap dan CopyOnWriteArrayList. |

---

## Latihan 3 — Simulasi Q&A

Minta teman/kolega mengajukan 3 pertanyaan tentang riset Anda. Catat pertanyaan dan evaluasi jawaban Anda.

| # | Pertanyaan | Jawaban Saya | Evaluasi |
|---|------------|--------------|----------|
| 1 | "Mengapa ArrayList.iterate pada 10⁶ elemen setara (TIE) dengan HashMap?" | "Pada ukuran dataset 10⁶, overhead cache miss pada ArrayList mulai setara dengan overhead hashing pada HashMap, sehingga perbedaan performa keduanya menjadi tidak signifikan." | [✓] Direct [✓] Data-based [✓] Honest |
| 2 | "Bagaimana cara mendeteksi outlier dalam data benchmark Anda?" | "Kami menggunakan deteksi outlier berbasis Z-score dengan threshold \|z\| > 3 pada setiap grup kombinasi, dan hasil menunjukkan tidak ada outlier ekstrem pada data bersih." | [✓] Direct [✓] Data-based [✓] Honest |
| 3 | "Apakah hasil visualisasi decision matrix Anda bisa langsung diterapkan pada sistem concurrency?" | "Tidak, karena benchmark ini single-threaded. Untuk multithreading, performa akan dipengaruhi oleh locking overhead, sehingga kami merekomendasikan ConcurrentHashMap." | [✓] Direct [✓] Data-based [✓] Honest |

**Pertanyaan yang paling sulit dijawab:**
> Bagaimana pengaruh arsitektur memori hardware (seperti ukuran cache L1/L2/L3) secara spesifik terhadap throughput ArrayList vs HashMap pada dataset sangat besar (1M+)?

**Apa yang perlu disiapkan lebih baik:**
> Mempelajari dokumentasi arsitektur CPU cache, menganalisis cache miss menggunakan profiler hardware, serta melakukan benchmark tambahan di mesin dengan spesifikasi hardware berbeda.

---

## Refleksi

> Dari seluruh proses WS-01 sampai WS-16 — dari paradigma riset hingga presentasi — bagian mana yang paling mengubah cara Anda berpikir tentang riset? Apa satu hal yang akan selalu Anda terapkan di riset berikutnya?

**Insight terbesar:**
> Pentingnya kejujuran metodologi riset (reproducibility) dan penerapan statistik inferensial (seperti ANOVA, Tukey HSD, Bonferroni) daripada sekadar berasumsi berdasarkan intuisi teoretis atau melihat rata-rata numerik mentah saja.

**Yang akan selalu diterapkan:**
> Selalu menggunakan framework formal (seperti JMH) untuk menjamin akurasi mikrobenchmark Java dengan memitigasi JVM bias, serta menyertakan visualisasi decision matrix yang praktis bagi pembaca.
