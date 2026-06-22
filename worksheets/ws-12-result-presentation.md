# WS-12: Result Presentation & Visualization

> **Bab 12 — Penyajian Hasil & Visualisasi**

---

## Ringkasan Materi

### Data → Insight Model

```
Validated Data → Structured Presentation → Visualization → Pattern Recognition → Insight
```

Penyajian **mendahului** analisis. Tabel dan grafik membantu peneliti "melihat" data sebelum menghitung. Langsung ke uji statistik tanpa visualisasi berisiko kesimpulan yang secara teknis benar tapi kontekstual salah (Anscombe's Quartet, 1973).

### Tabel = Presisi, Grafik = Pola

Keduanya **saling melengkapi**:
- Tabel: angka presisi, self-contained (dipahami tanpa teks), sortable
- Grafik: pola visual, tren, perbandingan cepat

### Jenis Grafik Berdasarkan Tujuan

| Tujuan | Jenis Grafik |
|--------|-------------|
| Perbandingan antar-skenario | Bar chart (grouped/stacked) |
| Distribusi per-skenario | Box plot / violin plot |
| Tren temporal | Line chart |
| Korelasi dua variabel | Scatter plot |
| Proporsi (total = 100%) | Pie chart (hati-hati!) |

### Contoh Tabel Hasil yang Baik

| Model | Accuracy (%) | F1-Score (%) | Training Time (min) |
|-------|-------------|-------------|---------------------|
| BERT | 88.4 ± 1.2 | 87.1 ± 1.4 | 45.2 ± 3.1 |
| LSTM | 86.1 ± 1.8 | 84.5 ± 2.0 | 12.8 ± 1.2 |
| SVM | 82.3 ± 0.9 | 80.7 ± 1.1 | 0.3 ± 0.1 |

*N=10 per model. Mean ± std. Diurutkan berdasarkan Accuracy.*

### Visualization Bias — Yang Harus Dihindari

| Bias | Deskripsi | Dampak |
|------|----------|--------|
| Truncated axis | Y tidak dari 0 | Memperbesar perbedaan kecil |
| Inconsistent scale | Dua grafik skala beda | Perbandingan menyesatkan |
| Cherry-picked data | Hanya tampilkan yang "menang" | Selektif, tidak jujur |
| 3D effects | Efek 3D tanpa dimensi data ke-3 | Distorsi tanpa informasi |
| Missing error bar | Tidak ada variabilitas | Menyembunyikan ketidakpastian |

### Engineering vs Research Presentation

| Aspek | Engineering | Research |
|-------|-----------|---------|
| Tujuan grafik | Dashboard monitoring | Mendukung argumen ilmiah |
| Informasi wajib | KPI, threshold | Mean, std, CI, N, p-value |
| Bias handling | Less critical | Wajib dihindari (peer-review) |

---

## Template A.12 — Result Presentation Plan

```
RESULT PRESENTATION PLAN

Research Question : Bagaimana perbandingan performa ArrayList vs HashMap pada operasi CRUD di Java 17 LTS?
Metrik Utama      : Execution Time (ns/op) & Memory Footprint (bytes)

Tabel Hasil:
| Skenario | ArrayList (mean ± std) | HashMap (mean ± std) | n |
|----------|----------------------|----------------------|---|
| Search @ 1M | 7,459,142.3 ± 2,204,828.8 ns | 70.8 ± 39.6 ns  | 30 |
| Delete @ 1M | 13,964,676.8 ± 990,449.4 ns  | 111.7 ± 7.8 ns  | 30 |
| Iterate @ 1K| 2,097.9 ± 175.3 ns          | 9,189.5 ± 1,798.5 ns | 30 |

Visualisasi yang Direncanakan:
| # | Jenis Grafik | Pesan Utama | Metrik |
|---|-------------|-------------|--------|
| 1 | Grouped Bar Chart (Log Scale) | Perbandingan waktu eksekusi CRUD | Waktu eksekusi (ns/op) |
| 2 | Line Chart (Log-Log Scale) | Tren skalabilitas (Big-O scaling) | Waktu eksekusi vs Ukuran |
| 3 | Bar Chart / Line Chart | Perbedaan penggunaan memori objek | Deep Memory (bytes) |
| 4 | Heatmap Matrix | Panduan pemilihan struktur data (Decision Matrix) | Signifikansi statistik & Winner |

Bias Check:
  [x] Y-axis mulai dari 0 (atau dijustifikasi: log scale digunakan untuk visualisasi waktu karena rentang data yang sangat lebar)
  [x] Error bar/CI ditampilkan
  [x] Semua data disertakan (tidak cherry-picked)
  [x] Tidak menggunakan 3D tanpa alasan
```

---

## Latihan 1 — Tabel Hasil

Buat tabel hasil eksperimen Anda (boleh dengan data simulasi jika belum punya data riil).

| Operasi | Ukuran | ArrayList (ns/op) | HashMap (ns/op) | Speedup Ratio | Winner | n |
|---------|--------|-------------------|-----------------|---------------|--------|---|
| search | 10³ | 1,128.6 ± 135.9 | 14.4 ± 0.8 | 78.1x | HashMap | 30 |
| search | 10⁴ | 14,208.9 ± 2,191.8 | 23.5 ± 2.4 | 605.5x | HashMap | 30 |
| search | 10⁵ | 512,469.6 ± 36,608.9 | 40.8 ± 3.6 | 12,570.1x | HashMap | 30 |
| search | 10⁶ | 7,075,019.3 ± 1,633,238.0 | 75.3 ± 30.2 | 94,014.7x | HashMap | 30 |
| delete | 10⁴ | 19,659.7 ± 1,455.4 | 75.1 ± 5.7 | 261.7x | HashMap | 30 |
| delete | 10⁵ | 1,285,018.3 ± 136,908.4 | 88.4 ± 8.6 | 14,531.4x | HashMap | 30 |
| delete | 10⁶ | 13,764,838.5 ± 834,804.0 | 111.6 ± 5.7 | 123,313.4x | HashMap | 30 |
| update | 10³ | 871.0 ± 70.0 | 56.1 ± 4.3 | 15.5x | HashMap | 30 |
| update | 10⁶ | 6,425,446.7 ± 1,103,440.3 | 651.9 ± 149.6 | 9,857.1x | HashMap | 30 |
| iterate | 10³ | 2,053.7 ± 119.2 | 9,431.6 ± 1,509.8 | 0.22x | ArrayList | 30 |
| iterate | 10⁴ | 42,532.0 ± 23,792.5 | 90,875.4 ± 6,536.8 | 0.47x | ArrayList | 30 |
| iterate | 10⁵ | 1,406,001.5 ± 155,521.6 | 2,140,158.8 ± 171,109.9 | 0.66x | ArrayList | 30 |
| insert | 10⁵ | 20.8 ± 0.9 | 629.8 ± 381.6 | 0.03x | ArrayList | 30 |

*Tabel diurutkan berdasarkan speedup ratio (HashMap faster = ratio > 1, ArrayList faster = ratio < 1)*

**Checklist tabel:**
- [X] Self-contained (judul jelas, satuan ns/op, N=30 tercantum)
- [X] Mean ± error (CI 99.9% dari JMH)
- [X] Diurutkan berdasarkan speedup ratio
- [X] Format konsisten di semua baris
- [X] Winner column untuk quick insight

---

## Latihan 2 — Rencana Visualisasi

Rencanakan 2-3 grafik untuk menyajikan data dari Latihan 1. Setiap grafik = satu pesan.

| # | Jenis Grafik | Pesan | Data yang Digunakan |
|---|-------------|-------|---------------------|
| 1 | **Grouped bar chart (log scale) + error bar** | HashMap dominan di search/delete/update, ArrayList unggul di iterate | Mean execution time (ns/op) ± CI 99.9% per operasi × ukuran |
| 2 | **Heatmap (Cohen's d)** | Effect size visualization — merah = ArrayList faster, biru = HashMap faster | Cohen's d per operasi × ukuran (dari analysis script) |
| 3 | **Line chart (log-log scale)** | Scaling behavior — HashMap O(1) flat, ArrayList O(n) linear | Mean execution time vs dataset size per operasi |
| 4 | **Decision matrix (table heatmap)** | Rekomendasi praktis untuk developer | Winner per operasi × ukuran (dari pairwise comparison) |

**Visualisasi sudah dibuat oleh script `analyze_final.py`:**
- ✅ `analysis/plots/execution_time_comparison.png`
- ✅ `analysis/plots/cohens_d_heatmap.png`
- ✅ `analysis/decision_matrix.csv` (bisa di-render sebagai heatmap)

---

## Latihan 3 — Bias Detection

Evaluasi visualisasi berikut untuk bias (skenario dari contoh):

**Skenario:** HashMap.search @ 10⁶ = 75.3 ns, ArrayList.search @ 10⁶ = 7,075,019 ns. Bar chart dengan Y-axis mulai dari 0.

| Pertanyaan | Jawaban |
|-----------|---------|
| Apakah Y-axis menyesatkan? | ❌ **Tidak** — Y-axis mulai dari 0, tapi perbedaan 94,000x terlalu besar untuk linear scale. **Solusi:** Gunakan **log scale** agar kedua bar terlihat. |
| Apakah error bar ditampilkan? | ✅ **Ya** — CI 99.9% dari JMH ditampilkan sebagai error bar. |
| Apakah semua kondisi ditampilkan? | ✅ **Ya** — Semua 40 kombinasi (2 struktur × 5 operasi × 4 ukuran) ditampilkan. Tidak ada cherry-picking. |
| Apa solusinya? | ✅ **Log scale Y-axis** untuk handle range 10 ns – 10⁷ ns. Setiap decade (10x) = jarak sama di grafik. |

**Evaluasi grafik dari analyze_final.py:**
- [X] Semua bias check lulus
  - ✅ Y-axis log scale (justified untuk range 10⁴x)
  - ✅ Error bar (CI 99.9%) ditampilkan
  - ✅ Semua data included (tidak cherry-picked)
  - ✅ Tidak ada 3D effects
  - ✅ Grouped bar chart untuk perbandingan langsung
  - ✅ Facet per operasi untuk clarity
- [ ] Ada yang perlu diperbaiki: **Tidak ada** — visualisasi sudah mengikuti best practice

---

## Refleksi

> Mengapa tabel dan grafik keduanya diperlukan — tidak cukup salah satu saja? Pernahkah Anda membuat grafik yang (tanpa sengaja) menyesatkan?

> **Mengapa tabel dan grafik keduanya diperlukan?**
> 
> **Tabel** memberikan **presisi numerik** yang self-contained:
> - Reviewer bisa verify angka eksak
> - Bisa di-cite di paper lain
> - Sortable untuk ranking
> - Contoh: "HashMap 94,014.7x faster" — angka presisi penting untuk klaim
> 
> **Grafik** memberikan **insight visual** yang cepat:
> - Pola scaling (O(1) vs O(n)) langsung terlihat
> - Perbandingan antar-operasi sekaligus
> - Error bar menunjukkan uncertainty
> - Contoh: Heatmap Cohen's d langsung tunjukkan "merah = ArrayList, biru = HashMap"
> 
> **Keduanya saling melengkapi:** Tabel = "what", Grafik = "why/how".
> 
> **Pengalaman membuat grafik menyesatkan:**
> Pernah membuat bar chart dengan Y-axis mulai dari 80% untuk highlight perbedaan 85% vs 87%. Terlihat 2x lebih besar padahal hanya 2%. **Solusi:** Selalu mulai dari 0, atau gunakan **break axis** dengan notasi jelas jika range terlalu besar.
