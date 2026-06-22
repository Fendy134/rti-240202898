"""
02_statistical_analysis.py
===========================
Analisis statistik hasil benchmark sesuai proposal E.5:
  1. Descriptive statistics (mean, median, std, CI 99%)
  2. Shapiro-Wilk test (uji normalitas)
  3. Levene's test (uji homogeneity of variance)
  4. Two-way ANOVA (struktur data × operasi × ukuran)
  5. Tukey HSD post-hoc (pairwise comparison)
  6. Bonferroni correction (α = 0.05/20 = 0.0025)
  7. Cohen's d (effect size: medium > 0.5, large > 0.8)

Input  : results/clean_data.csv   (output dari 01_validate_data.py)
Output : results/stats_report.txt
         results/descriptive_stats.csv
         results/anova_results.csv
         results/pairwise_comparison.csv
         results/effect_sizes.csv

Cara pakai:
  pip install pandas scipy statsmodels pingouin
  python 02_statistical_analysis.py results/clean_data.csv
"""

import sys
import warnings
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

warnings.filterwarnings("ignore")

# ── Konstanta sesuai proposal ─────────────────────────────────────────────────
ALPHA            = 0.05
N_COMPARISONS    = 20                        # total pairwise comparisons
ALPHA_BONFERRONI = ALPHA / N_COMPARISONS     # = 0.0025
CI_LEVEL         = 0.99                      # CI 99%

# Cohen's d threshold
COHENS_D_MEDIUM = 0.5
COHENS_D_LARGE  = 0.8


# ── Helper ────────────────────────────────────────────────────────────────────
def section(title):
    line = "=" * 65
    print(f"\n{line}\n  {title}\n{line}")

def fmt_p(p):
    """Format p-value dengan tanda signifikansi."""
    if p < 0.001:  return f"{p:.2e} ***"
    if p < 0.01:   return f"{p:.4f} **"
    if p < 0.05:   return f"{p:.4f} *"
    return f"{p:.4f} ns"


# ── Load data ─────────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Filter hanya avgt (primary DV: execution time ns/op)
    avgt = df[df["mode"] == "avgt"].copy()
    avgt["log_score"] = np.log(avgt["score"])   # log-transform untuk ANOVA
    return avgt


# ── 1. Descriptive Statistics ─────────────────────────────────────────────────
def descriptive_stats(df: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    section("1. DESCRIPTIVE STATISTICS (ns/op, CI 99%)")

    results = []
    for (cls, op, size), group in df.groupby(["class_name", "operation", "dataset_size"]):
        scores = group["score"].dropna()
        n      = len(scores)
        mean   = scores.mean()
        median = scores.median()
        std    = scores.std()
        sem    = stats.sem(scores)
        ci     = stats.t.interval(CI_LEVEL, df=n-1, loc=mean, scale=sem)

        results.append({
            "structure"   : cls.replace("Benchmark", ""),
            "operation"   : op,
            "dataset_size": size,
            "n"           : n,
            "mean_ns"     : round(mean, 2),
            "median_ns"   : round(median, 2),
            "std_ns"      : round(std, 2),
            "ci99_low"    : round(ci[0], 2),
            "ci99_high"   : round(ci[1], 2),
            "cv_pct"      : round((std / mean) * 100, 2),
        })

    desc_df = pd.DataFrame(results)

    # Print ringkasan per operasi
    for op in ["insert", "search", "update", "delete", "iterate"]:
        print(f"\n  Operasi: {op.upper()}")
        print(f"  {'Structure':<12} {'Size':>8} {'Mean (ns)':>12} "
              f"{'Std':>10} {'CI99 Low':>12} {'CI99 High':>12} {'CV%':>6}")
        print("  " + "-" * 75)
        subset = desc_df[desc_df["operation"] == op].sort_values(
            ["structure", "dataset_size"])
        for _, row in subset.iterrows():
            print(f"  {row['structure']:<12} {row['dataset_size']:>8,} "
                  f"{row['mean_ns']:>12,.1f} {row['std_ns']:>10,.1f} "
                  f"{row['ci99_low']:>12,.1f} {row['ci99_high']:>12,.1f} "
                  f"{row['cv_pct']:>6.1f}")

    path = out_dir / "descriptive_stats.csv"
    desc_df.to_csv(path, index=False)
    print(f"\n  → Disimpan: {path}")
    return desc_df


# ── 2. Uji Normalitas (Shapiro-Wilk) ─────────────────────────────────────────
def test_normality(df: pd.DataFrame) -> bool:
    section("2. UJI NORMALITAS — Shapiro-Wilk (H0: data normal)")

    all_normal = True
    print(f"\n  {'Group':<45} {'W':>8} {'p-value':>14} {'Normal?':>8}")
    print("  " + "-" * 80)

    for (cls, op, size), group in df.groupby(["class_name", "operation", "dataset_size"]):
        scores = group["score"].dropna()
        if len(scores) < 3:
            continue
        w, p = stats.shapiro(scores)
        is_normal = p >= ALPHA
        if not is_normal:
            all_normal = False
        label = f"{cls.replace('Benchmark','')}.{op} n={size:,}"
        print(f"  {label:<45} {w:>8.4f} {fmt_p(p):>14} {'YES' if is_normal else 'NO':>8}")

    if not all_normal:
        print("\n  [INFO] Data tidak sepenuhnya normal.")
        print("         ANOVA robust terhadap deviasi normalitas (Central Limit Theorem).")
        print("         Log-transform akan dipakai untuk meningkatkan normalitas.")

    return all_normal


# ── 3. Uji Homogeneity of Variance (Levene) ──────────────────────────────────
def test_homogeneity(df: pd.DataFrame) -> bool:
    section("3. UJI HOMOGENEITY OF VARIANCE — Levene's Test")

    all_homogen = True
    print(f"\n  {'Operasi':<15} {'F-stat':>10} {'p-value':>14} {'Homogen?':>10}")
    print("  " + "-" * 55)

    for op in df["operation"].unique():
        groups = [
            grp["score"].dropna().values
            for _, grp in df[df["operation"] == op].groupby("class_name")
        ]
        if len(groups) < 2:
            continue
        f, p = stats.levene(*groups)
        is_homogen = p >= ALPHA
        if not is_homogen:
            all_homogen = False
        print(f"  {op:<15} {f:>10.4f} {fmt_p(p):>14} {'YES' if is_homogen else 'NO':>10}")

    return all_homogen


# ── 4. Two-way ANOVA ──────────────────────────────────────────────────────────
def run_anova(df: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    section("4. TWO-WAY ANOVA (log-transformed execution time)")

    df = df.copy()
    df["structure"]    = df["class_name"].str.replace("Benchmark", "")
    df["size_cat"]     = df["dataset_size"].astype(str)   # kategorikal

    # Formula: log(score) ~ struktur * operasi * ukuran
    formula = "log_score ~ C(structure) + C(operation) + C(size_cat) " \
              "+ C(structure):C(operation) " \
              "+ C(structure):C(size_cat) " \
              "+ C(operation):C(size_cat)"

    model  = ols(formula, data=df).fit()
    anova_table = anova_lm(model, typ=2)

    print("\n  Two-way ANOVA Table (Type II SS):")
    print(f"\n  {'Source':<40} {'F':>10} {'p-value':>16}")
    print("  " + "-" * 70)

    anova_results = []
    for source, row in anova_table.iterrows():
        p    = row["PR(>F)"]
        f    = row["F"]
        sig  = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
        print(f"  {source:<40} {f:>10.4f} {p:>10.4f} {sig:>5}")
        anova_results.append({
            "source"    : source,
            "F"         : round(f, 4),
            "p_value"   : round(p, 6),
            "significant": p < ALPHA,
        })

    anova_df = pd.DataFrame(anova_results)
    path = out_dir / "anova_results.csv"
    anova_df.to_csv(path, index=False)
    print(f"\n  → Disimpan: {path}")
    print(f"\n  R² = {model.rsquared:.4f}  |  Adj. R² = {model.rsquared_adj:.4f}")

    return anova_df


# ── 5 & 6. Tukey HSD + Bonferroni ────────────────────────────────────────────
def run_posthoc(df: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    section("5 & 6. POST-HOC — Tukey HSD + Bonferroni Correction")

    df = df.copy()
    df["structure"] = df["class_name"].str.replace("Benchmark", "")
    df["group"]     = df["structure"] + "_" + df["operation"] + "_" + df["dataset_size"].astype(str)

    # Tukey HSD
    tukey = pairwise_tukeyhsd(
        endog  = df["log_score"],
        groups = df["group"],
        alpha  = ALPHA_BONFERRONI      # pakai alpha yang sudah di-correct
    )

    # Fokus: ArrayList vs HashMap untuk tiap operasi × ukuran
    pairs = []
    operations = df["operation"].unique()
    sizes      = sorted(df["dataset_size"].unique())

    print(f"\n  α Bonferroni-corrected = {ALPHA:.2f}/{N_COMPARISONS} = {ALPHA_BONFERRONI:.4f}")
    print(f"\n  {'Operasi':<10} {'Size':>8} {'AL mean':>12} {'HM mean':>12} "
          f"{'Diff%':>8} {'p-adj':>12} {'Sig?':>6}")
    print("  " + "-" * 75)

    for op in operations:
        for size in sizes:
            al = df[(df["structure"] == "ArrayList")  & (df["operation"] == op) &
                    (df["dataset_size"] == size)]["score"]
            hm = df[(df["structure"] == "HashMap")    & (df["operation"] == op) &
                    (df["dataset_size"] == size)]["score"]

            if len(al) == 0 or len(hm) == 0:
                continue

            al_mean = al.mean()
            hm_mean = hm.mean()
            diff_pct = ((al_mean - hm_mean) / al_mean) * 100  # positif = AL lebih lambat

            # Welch's t-test dengan Bonferroni correction
            t_stat, p_raw = stats.ttest_ind(al, hm, equal_var=False)
            p_bonf = min(p_raw * N_COMPARISONS, 1.0)           # Bonferroni correction
            sig    = p_bonf < ALPHA_BONFERRONI

            pairs.append({
                "operation"   : op,
                "dataset_size": size,
                "AL_mean_ns"  : round(al_mean, 2),
                "HM_mean_ns"  : round(hm_mean, 2),
                "diff_pct"    : round(diff_pct, 1),
                "t_stat"      : round(t_stat, 4),
                "p_raw"       : round(p_raw, 6),
                "p_bonferroni": round(p_bonf, 6),
                "significant" : sig,
                "faster"      : "HashMap" if hm_mean < al_mean else "ArrayList",
            })

            print(f"  {op:<10} {size:>8,} {al_mean:>12,.1f} {hm_mean:>12,.1f} "
                  f"{diff_pct:>+7.1f}% {p_bonf:>10.4f} {'YES' if sig else 'NO':>6}")

    pairs_df = pd.DataFrame(pairs)
    path = out_dir / "pairwise_comparison.csv"
    pairs_df.to_csv(path, index=False)
    print(f"\n  → Disimpan: {path}")
    return pairs_df


# ── 7. Cohen's d ──────────────────────────────────────────────────────────────
def compute_effect_sizes(df: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    section("7. EFFECT SIZE — Cohen's d")

    df = df.copy()
    df["structure"] = df["class_name"].str.replace("Benchmark", "")

    print(f"\n  Threshold: medium d > {COHENS_D_MEDIUM}, large d > {COHENS_D_LARGE}")
    print(f"\n  {'Operasi':<10} {'Size':>8} {'Cohen d':>10} {'Effect':>10} {'Interpretation':>30}")
    print("  " + "-" * 75)

    results = []
    for op in df["operation"].unique():
        for size in sorted(df["dataset_size"].unique()):
            al = df[(df["structure"] == "ArrayList") & (df["operation"] == op) &
                    (df["dataset_size"] == size)]["score"].dropna()
            hm = df[(df["structure"] == "HashMap")   & (df["operation"] == op) &
                    (df["dataset_size"] == size)]["score"].dropna()

            if len(al) < 2 or len(hm) < 2:
                continue

            # Pooled standard deviation
            n1, n2   = len(al), len(hm)
            s_pooled = np.sqrt(((n1-1)*al.std()**2 + (n2-1)*hm.std()**2) / (n1+n2-2))
            d        = abs(al.mean() - hm.mean()) / s_pooled if s_pooled > 0 else 0

            if d >= COHENS_D_LARGE:
                effect = "LARGE"
                interp = "Perbedaan sangat praktis signifikan"
            elif d >= COHENS_D_MEDIUM:
                effect = "MEDIUM"
                interp = "Perbedaan cukup praktis signifikan"
            else:
                effect = "SMALL"
                interp = "Perbedaan kurang praktis signifikan"

            results.append({
                "operation"   : op,
                "dataset_size": size,
                "cohens_d"    : round(d, 4),
                "effect_size" : effect,
                "meets_h1"    : d > COHENS_D_MEDIUM,
            })

            print(f"  {op:<10} {size:>8,} {d:>10.4f} {effect:>10} {interp:>30}")

    eff_df = pd.DataFrame(results)
    path   = out_dir / "effect_sizes.csv"
    eff_df.to_csv(path, index=False)
    print(f"\n  → Disimpan: {path}")
    return eff_df


# ── Summary & Kesimpulan ──────────────────────────────────────────────────────
def print_summary(pairs_df: pd.DataFrame, eff_df: pd.DataFrame):
    section("SUMMARY — KESIMPULAN TERHADAP HIPOTESIS")

    print("""
  H₁ yang diuji:
    H₁a: HashMap lebih cepat di search (Cohen's d > 0.8)
    H₁b: ArrayList lebih cepat di iterate (Cohen's d > 0.5)
    H₁c: ArrayList lebih hemat memori pada dataset kecil (>10%)
  """)

    # H1a: search
    search_eff = eff_df[eff_df["operation"] == "search"]
    h1a_met    = (search_eff["cohens_d"] > COHENS_D_LARGE).any()
    search_sig = pairs_df[
        (pairs_df["operation"] == "search") &
        (pairs_df["faster"] == "HashMap") &
        (pairs_df["significant"] == True)
    ]
    print(f"  H₁a (search): {'✓ DITERIMA' if h1a_met and len(search_sig) > 0 else '✗ DITOLAK'}")
    if len(search_sig) > 0:
        print(f"       HashMap lebih cepat pada {len(search_sig)} kombinasi size, "
              f"max diff = {search_sig['diff_pct'].max():.1f}%")

    # H1b: iterate
    iter_eff = eff_df[eff_df["operation"] == "iterate"]
    h1b_met  = (iter_eff["cohens_d"] > COHENS_D_MEDIUM).any()
    iter_sig = pairs_df[
        (pairs_df["operation"] == "iterate") &
        (pairs_df["faster"] == "ArrayList") &
        (pairs_df["significant"] == True)
    ]
    print(f"\n  H₁b (iterate): {'✓ DITERIMA' if h1b_met and len(iter_sig) > 0 else '✗ DITOLAK'}")
    if len(iter_sig) > 0:
        print(f"       ArrayList lebih cepat pada {len(iter_sig)} kombinasi size, "
              f"max diff = {iter_sig['diff_pct'].abs().max():.1f}%")

    print(f"\n  H₁c (memory): Lihat hasil MemoryProfiler → results/memory_footprint.csv")
    print(f"\n  α Bonferroni-corrected = {ALPHA_BONFERRONI:.4f}")
    print(f"  Significance level     = p < {ALPHA_BONFERRONI:.4f}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python 02_statistical_analysis.py results/clean_data.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    out_dir  = Path(csv_path).parent

    print(f"\n{'#'*65}")
    print(f"  STATISTICAL ANALYSIS REPORT")
    print(f"  Input  : {csv_path}")
    print(f"  α      : {ALPHA}  |  α Bonferroni : {ALPHA_BONFERRONI:.4f}")
    print(f"  CI     : {int(CI_LEVEL*100)}%")
    print(f"{'#'*65}")

    df = load_data(csv_path)
    print(f"\n  Data dimuat: {len(df)} baris (mode=avgt)")

    desc_df  = descriptive_stats(df, out_dir)
    test_normality(df)
    test_homogeneity(df)
    anova_df = run_anova(df, out_dir)
    pairs_df = run_posthoc(df, out_dir)
    eff_df   = compute_effect_sizes(df, out_dir)
    print_summary(pairs_df, eff_df)

    print(f"\n{'='*65}")
    print(f"  Analisis selesai. Output di: {out_dir}")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
