"""
01_validate_data.py
===================
Validasi data hasil JMH benchmark sebelum analisis statistik.

Sesuai proposal E.3 — 5 tahap validasi:
  1. Completeness   : semua 120 runs terkumpul
  2. Consistency    : tidak ada kontradiksi internal
  3. Validity       : metrik mengukur apa yang dimaksud
  4. Representativeness: data mewakili target
  5. Outlier check  : deteksi nilai ekstrem per grup

Input  : results/jmh_result_*.csv  (output JMH)
Output : results/validation_report.txt
         results/clean_data.csv    (siap untuk analisis)

Cara pakai:
  pip install pandas scipy
  python 01_validate_data.py results/jmh_result_TIMESTAMP.csv
"""

import sys
import re
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

# ── Konstanta sesuai proposal ─────────────────────────────────────────────────
EXPECTED_STRUCTURES = {"ArrayListBenchmark", "HashMapBenchmark"}
EXPECTED_OPERATIONS = {"insert", "search", "update", "delete", "iterate"}
EXPECTED_SIZES      = {1000, 10000, 100000, 1000000}
EXPECTED_MODES      = {"avgt", "thrpt"}
EXPECTED_FORKS      = 3
EXPECTED_ITERATIONS = 10
# Total runs = 2 struktur × 5 operasi × 4 ukuran × 2 mode = 80 baris agregat
# (JMH CSV sudah diagregat per kombinasi)
EXPECTED_ROWS = 2 * 5 * 4 * 2   # = 80

OUTLIER_ZSCORE_THRESHOLD = 3.0   # |z| > 3 → outlier


# ── Helper ────────────────────────────────────────────────────────────────────
def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def ok(msg):   print(f"  [OK]   {msg}")
def warn(msg): print(f"  [WARN] {msg}")
def fail(msg): print(f"  [FAIL] {msg}")


# ── Load & parse CSV JMH ──────────────────────────────────────────────────────
def load_jmh_csv(path: str) -> pd.DataFrame:
    """
    JMH CSV format:
      "Benchmark","Mode","Threads","Samples","Score","Score Error (99.9%)","Unit","Param: datasetSize"
    """
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.replace('"', '')

    # Normalkan nama kolom
    df.rename(columns={
        "Benchmark"           : "benchmark",
        "Mode"                : "mode",
        "Score"               : "score",
        "Score Error (99.9%)" : "score_error",
        "Unit"                : "unit",
        "Param: datasetSize"  : "dataset_size",
    }, inplace=True)

    # Ekstrak: class name dan method name dari benchmark
    # Format: com.research.benchmark.ArrayListBenchmark.insert
    df["class_name"] = df["benchmark"].apply(
        lambda x: re.search(r'(\w+Benchmark)', x).group(1) if re.search(r'(\w+Benchmark)', x) else None
    )
    df["operation"] = df["benchmark"].apply(
        lambda x: x.rsplit(".", 1)[-1]
    )
    df["dataset_size"] = df["dataset_size"].astype(int)
    df["score"]        = pd.to_numeric(df["score"], errors="coerce")
    df["score_error"]  = pd.to_numeric(df["score_error"], errors="coerce")

    return df


# ── Tahap 1: Completeness ─────────────────────────────────────────────────────
def check_completeness(df: pd.DataFrame) -> bool:
    section("TAHAP 1 — Completeness")
    passed = True

    # Cek struktur
    found_structures = set(df["class_name"].unique())
    missing = EXPECTED_STRUCTURES - found_structures
    if missing:
        fail(f"Struktur data tidak ditemukan: {missing}")
        passed = False
    else:
        ok(f"Semua struktur data ada: {found_structures}")

    # Cek operasi
    found_ops = set(df["operation"].unique())
    missing_ops = EXPECTED_OPERATIONS - found_ops
    if missing_ops:
        fail(f"Operasi tidak ditemukan: {missing_ops}")
        passed = False
    else:
        ok(f"Semua operasi ada: {found_ops}")

    # Cek ukuran dataset
    found_sizes = set(df["dataset_size"].unique())
    missing_sizes = EXPECTED_SIZES - found_sizes
    if missing_sizes:
        fail(f"Ukuran dataset tidak ditemukan: {missing_sizes}")
        passed = False
    else:
        ok(f"Semua ukuran dataset ada: {found_sizes}")

    # Cek jumlah baris
    actual_rows = len(df)
    if actual_rows < EXPECTED_ROWS:
        fail(f"Jumlah baris: {actual_rows} (expected ≥ {EXPECTED_ROWS})")
        passed = False
    else:
        ok(f"Jumlah baris: {actual_rows} (expected {EXPECTED_ROWS})")

    # Cek missing values
    null_counts = df[["score", "score_error", "dataset_size"]].isnull().sum()
    if null_counts.any():
        fail(f"Missing values ditemukan:\n{null_counts[null_counts > 0]}")
        passed = False
    else:
        ok("Tidak ada missing values pada kolom utama")

    return passed


# -- Tahap 2: Consistency ------------------------------------------------------
def check_consistency(df: pd.DataFrame) -> bool:
    section("TAHAP 2 - Consistency")
    passed = True

    # Score harus positif
    neg_scores = df[df["score"] < 0]
    if len(neg_scores) > 0:
        fail(f"Score < 0 ditemukan ({len(neg_scores)} baris):")
        print(neg_scores[["benchmark", "dataset_size", "mode", "score"]])
        passed = False
    else:
        ok("Semua score >= 0")

    # Score error tidak boleh lebih besar dari score itu sendiri
    bad_error = df[df["score_error"] > df["score"]]
    if len(bad_error) > 0:
        warn(f"Score error > score pada {len(bad_error)} baris - CI sangat lebar")
        print(bad_error[["benchmark", "dataset_size", "mode", "score", "score_error"]])
    else:
        ok("Score error < score pada semua baris")

    # Unit harus konsisten per mode
    for mode in df["mode"].unique():
        units = df[df["mode"] == mode]["unit"].unique()
        if len(units) > 1:
            fail(f"Unit tidak konsisten untuk mode '{mode}': {units}")
            passed = False
        else:
            ok(f"Unit konsisten untuk mode '{mode}': {units[0]}")

    return passed


# ── Tahap 3: Validity ─────────────────────────────────────────────────────────
def check_validity(df: pd.DataFrame) -> bool:
    section("TAHAP 3 — Validity")
    passed = True

    avgt  = df[df["mode"] == "avgt"]
    thrpt = df[df["mode"] == "thrpt"]

    # avgt harus dalam ns/op
    if len(avgt) > 0:
        units = avgt["unit"].unique()
        if not all("ns" in u for u in units):
            fail(f"avgt bukan ns/op: {units}")
            passed = False
        else:
            ok(f"avgt unit: {units[0]} ✓")

    # thrpt harus dalam ops/s atau ops/ns
    if len(thrpt) > 0:
        units = thrpt["unit"].unique()
        if not all("ops" in u for u in units):
            fail(f"thrpt bukan ops/*: {units}")
            passed = False
        else:
            ok(f"thrpt unit: {units[0]} ✓")

    # Sanity check: HashMap search HARUS lebih cepat dari ArrayList search
    # (avgt lebih kecil = lebih cepat)
    al_search = avgt[(avgt["class_name"] == "ArrayListBenchmark") &
                     (avgt["operation"] == "search")]["score"].mean()
    hm_search = avgt[(avgt["class_name"] == "HashMapBenchmark") &
                     (avgt["operation"] == "search")]["score"].mean()

    if al_search > 0 and hm_search > 0:
        ratio = al_search / hm_search
        if hm_search < al_search:
            ok(f"Sanity check search: HashMap ({hm_search:.0f} ns) "
               f"< ArrayList ({al_search:.0f} ns) — ratio {ratio:.1f}x ✓")
        else:
            warn(f"Sanity check search: HashMap ({hm_search:.0f} ns) "
                 f">= ArrayList ({al_search:.0f} ns) — periksa data!")

    return passed


# ── Tahap 4: Representativeness ───────────────────────────────────────────────
def check_representativeness(df: pd.DataFrame) -> bool:
    section("TAHAP 4 — Representativeness")
    passed = True

    avgt = df[df["mode"] == "avgt"]

    # Cek scaling: operasi O(n) harus scale dengan dataset size
    print("\n  Scaling check — avgt search (harus naik untuk ArrayList):")
    al_search = avgt[(avgt["class_name"] == "ArrayListBenchmark") &
                     (avgt["operation"] == "search")].sort_values("dataset_size")
    if len(al_search) >= 2:
        for _, row in al_search.iterrows():
            print(f"    size={row['dataset_size']:>8,} → {row['score']:>12.1f} ns/op")

        # Verifikasi monoton naik (toleransi 10%)
        scores = al_search["score"].values
        is_monotone = all(scores[i] <= scores[i+1] * 1.1 for i in range(len(scores)-1))
        if is_monotone:
            ok("ArrayList search scaling monoton naik sesuai O(n) ✓")
        else:
            warn("ArrayList search tidak monoton naik — periksa data")

    # HashMap search harus relatif flat
    print("\n  Scaling check — avgt search (harus relatif flat untuk HashMap):")
    hm_search = avgt[(avgt["class_name"] == "HashMapBenchmark") &
                     (avgt["operation"] == "search")].sort_values("dataset_size")
    if len(hm_search) >= 2:
        for _, row in hm_search.iterrows():
            print(f"    size={row['dataset_size']:>8,} → {row['score']:>12.1f} ns/op")
        scores = hm_search["score"].values
        cv = np.std(scores) / np.mean(scores)
        if cv < 0.3:
            ok(f"HashMap search relatif flat (CV={cv:.2f}) sesuai O(1) ✓")
        else:
            warn(f"HashMap search CV={cv:.2f} — variasi tinggi, periksa data")

    return passed


# ── Tahap 5: Outlier Detection ────────────────────────────────────────────────
def check_outliers(df: pd.DataFrame) -> pd.DataFrame:
    section("TAHAP 5 — Outlier Detection (|z| > 3)")

    avgt = df[df["mode"] == "avgt"].copy()
    outlier_flags = []

    for (cls, op, size), group in avgt.groupby(["class_name", "operation", "dataset_size"]):
        if len(group) < 2:
            continue
        z = np.abs(stats.zscore(group["score"].dropna()))
        outliers = group[z > OUTLIER_ZSCORE_THRESHOLD]
        if len(outliers) > 0:
            warn(f"Outlier: {cls}.{op} size={size:,} → {len(outliers)} baris")
            outlier_flags.extend(outliers.index.tolist())

    if not outlier_flags:
        ok("Tidak ada outlier terdeteksi (|z| ≤ 3 pada semua grup)")

    # Tandai outlier di dataframe
    df["is_outlier"] = df.index.isin(outlier_flags)
    n_outliers = df["is_outlier"].sum()
    print(f"\n  Total outlier: {n_outliers} dari {len(df)} baris")

    return df


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python 01_validate_data.py <path_to_jmh_result.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    out_dir  = Path(csv_path).parent

    print(f"\n{'#'*60}")
    print(f"  DATA VALIDATION REPORT")
    print(f"  Input : {csv_path}")
    print(f"{'#'*60}")

    # Load
    df = load_jmh_csv(csv_path)
    print(f"\n  Loaded {len(df)} baris dari {csv_path}")

    # Jalankan semua tahap validasi
    c1 = check_completeness(df)
    c2 = check_consistency(df)
    c3 = check_validity(df)
    c4 = check_representativeness(df)
    df = check_outliers(df)

    # Summary
    section("SUMMARY")
    all_passed = all([c1, c2, c3, c4])
    if all_passed:
        ok("Semua tahap validasi LULUS — data siap untuk analisis statistik")
    else:
        warn("Ada tahap yang GAGAL — periksa detail di atas sebelum lanjut")

    # Simpan clean data (tanpa outlier)
    clean_df = df[~df["is_outlier"]].copy()
    clean_path = out_dir / "clean_data.csv"
    clean_df.to_csv(clean_path, index=False)
    print(f"\n  Clean data disimpan: {clean_path}")
    print(f"  Baris: {len(df)} total → {len(clean_df)} setelah remove outlier")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
