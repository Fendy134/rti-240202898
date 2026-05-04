# WS-06: System-Experiment Mapping

> **Bab 6 — System Design sebagai Experimental Artifact**

---

## Ringkasan Materi

### Sistem = Instrumen Pengujian, Bukan Produk

Seorang engineer bertanya "apakah sistem bekerja?" — seorang peneliti bertanya "apa yang bisa dibuktikan sistem ini?" Sistem dalam riset adalah **artifact** — objek yang sengaja dibuat untuk menguji klaim spesifik.

### System as Experiment Model

```
RQ → Variable → System Component → Experimental Setup → Output
```

Setiap komponen sistem harus bisa ditelusuri ke variabel riset (top-down), dan setiap pengukuran harus menjawab RQ (bottom-up).

### Mapping Variabel ke Komponen

| Tipe Variabel | Peran di Sistem | Contoh |
|---------------|----------------|--------|
| **IV** (Independent) | Modul yang bisa di-toggle/swap | Algoritma A vs B |
| **DV** (Dependent) | Modul pengukuran | Logger, metrics collector |
| **CV** (Control) | Config yang dikunci | Dataset, parameter tetap |

Jika variabel tidak bisa di-map ke komponen apapun → arsitektur perlu didesain ulang.

### 4 Prinsip Desain Eksperimental

| Prinsip | Pertanyaan Kunci |
|---------|-----------------|
| **Traceability** | Komponen ini melayani variabel yang mana? |
| **Modularity** | Bisakah IV diubah tanpa memengaruhi yang lain? |
| **Controllability** | Apakah CV dieksternalisasi ke config file? |
| **Measurability** | Apakah sistem otomatis menghasilkan data yang dibutuhkan? |

### Variable Isolation melalui Arsitektur

- **Modular architecture** — Pisahkan berdasarkan variabel
- **Configuration-driven** — Ubah config (YAML/JSON), bukan code
- **Feature toggles** — On/off flag untuk ablation study

### Research vs Engineering

| Aspek | Engineering | Research |
|-------|------------|----------|
| Tujuan sistem | Memenuhi kebutuhan user | Menguji hipotesis, menghasilkan bukti |
| Arsitektur | Optimasi performa & skalabilitas | Optimasi isolasi variabel & reprodusibilitas |
| Konfigurasi | Sering hardcoded | Dieksternalisasi ke config file |
| Fitur tambahan | Menambah nilai user | Menambah noise jika tidak terkait RQ |

### Istilah Penting

- **Artifact** — Objek yang sengaja dibuat untuk memecahkan masalah atau menguji proposisi
- **Traceability** — Kemampuan menelusuri hubungan RQ → variabel → komponen → output
- **Variable Isolation** — Mengubah hanya satu variabel sambil menahan yang lain konstan
- **Ablation Study** — Menguji kontribusi tiap komponen dengan melepasnya satu per satu
- **Configuration-driven Execution** — Semua parameter di config file, bukan hardcoded

---

## Template A.6 — Mapping RQ ke Arsitektur Sistem

```
SYSTEM-EXPERIMENT MAPPING

Research Question: Apakah GA multi-objective menghasilkan solusi penjadwalan lebih optimal (makespan, energi, availability) dibanding GA single-objective dan metode manual pada kasus penjadwalan 30 produk di PT. Nuansa Indah?

Variable → Component Mapping:
| Variabel | Tipe | Komponen Sistem | Cara Manipulasi/Pengukuran |
|----------|------|-----------------|---------------------------|
| Metode penjadwalan | IV | Modul algoritma (GA multi-obj, GA single-obj, Manual FCFS) | Ganti config `scheduling_method` dan parameter objectives |
| Makespan | DV | Modul metrics collector & logger | Otomatis mencatat timestamp start/end setiap job |
| Konsumsi energi | DV | Modul energy tracker | Otomatis mengakumulasi energi per mesin per unit waktu |
| Availability mesin | DV | Modul availability monitor | Otomatis menghitung (uptime / total_time) × 100 |
| Jumlah produk | CV | Config file (`num_jobs: 30`) | Dikunci pada 30 produk untuk semua eksperimen |
| Jumlah mesin | CV | Config file (`num_machines: 5`) | Dikunci pada 5 mesin untuk semua eksperimen |
| Parameter GA | CV | Config file (population_size, generations, mutation_rate, crossover_rate) | Dikunci dengan nilai yang sama untuk semua metode GA |

4 Prinsip Desain:
  [X] Traceability — Setiap komponen bisa ditelusuri ke variabel
  [X] Variable Isolation — IV bisa diubah tanpa mengubah CV
  [X] Measurement Integration — Pengukuran DV built-in di modul logger
  [X] Reproducibility — Setup bisa direkonstruksi dari config file

Experimental Setup:
  Input data     : Data historis PT. Nuansa Indah (30 produk, 5 mesin, waktu standar per produk per mesin, daya mesin)
  Parameter      : scheduling_method (GA-multi, GA-single, Manual), population_size (100), generations (500), mutation_rate (0.1), crossover_rate (0.8), num_jobs (30), num_machines (5)
  Output format  : JSON dengan fields: method, makespan_minutes, energy_kwh, availability_percent, execution_time_seconds, timestamp
```

---

## Latihan 1 — Variable-to-Component Mapping

Gunakan RQ dan variabel dari WS-05. Petakan ke komponen sistem.

**RQ:** __________________________________________________

| Variabel | Tipe | Komponen Sistem | Cara Manipulasi / Pengukuran |
|----------|------|-----------------|---------------------------|
| *Contoh: Jenis model* | *IV* | *Modul classifier (swap RF ↔ CNN)* | *Ganti config `model_type`* |
| | DV | | |
| | CV | | |

**Apakah semua variabel bisa di-map?** [ ] Ya / [ ] Tidak
> Jika tidak, komponen apa yang perlu ditambahkan? _________

---

## Latihan 2 — 4 Prinsip Desain

Evaluasi desain sistem terhadap 4 prinsip.

| Prinsip | Status | Bukti / Penjelasan |
|---------|--------|-------------------|
| Traceability | *Contoh: ✅ — setiap modul punya label variabel* | |
| Modularity | | |
| Controllability | | |
| Measurability | | |

**Prinsip mana yang paling sulit dipenuhi?** _______________
**Strategi untuk mengatasinya:**
> ___________________________________________________

---

## Latihan 3 — Ablation Study Planning

Jika sistem memiliki 3 komponen utama, rencanakan ablation study.

| Kondisi | Komponen A | Komponen B | Komponen C | Hasil yang Diharapkan |
|---------|-----------|-----------|-----------|----------------------|
| Full | *Contoh: ✅ CNN* | *Contoh: ✅ Temporal features* | *Contoh: ✅ Z-score norm* | *Baseline penuh* |
| – A | ❌ (ganti RF) | ✅ | ✅ | |
| – B | ✅ | ❌ (tanpa temporal) | ✅ | |
| – C | ✅ | ✅ | ❌ (tanpa normalisasi) | |

**Komponen mana yang diprediksi paling berkontribusi?** _____
**Mengapa?**
> ___________________________________________________

---

## Refleksi

> Apa risiko jika sistem dibangun seperti produk (monolitik, fitur lengkap) lalu baru dilakukan eksperimen? Mengapa arsitektur modular penting untuk riset?

**Jawaban:**
> ___________________________________________________
> ___________________________________________________
