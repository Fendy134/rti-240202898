"""
03_visualize.py
===============
Visualisasi hasil benchmark + decision matrix sesuai proposal F.

Output:
  results/fig_execution_time.png   — heatmap ns/op per operasi × ukuran
  results/fig_speedup_ratio.png    — speedup HashMap vs ArrayList per operasi
  results/fig_memory_footprint.png — bar chart memory bytes/element
  results/fig_decision_matrix.png  — decision matrix praktis untuk developer
  results/decision_matrix.csv      — tabel rekomendasi struktur data

Cara pakai:
  pip install pandas matplotlib seaborn
  python 03_visualize.py results/
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family"   : "DejaVu Sans",
    "font.size"     : 11,
    "axes.titlesize": 13,
    "figure.dpi"    : 150,
})
COLORS = {
    "ArrayList": "#2196F3",   # biru
    "HashMap"  : "#FF5722",   # oranye-merah
    "neutral"  : "#9E9E9E",
    "win"      : "#4CAF50",   # hijau = lebih cepat
    "lose"     : "#F44336",   # merah = lebih lambat
}
SIZE_LABELS = ["1K", "10K", "100K", "1M"]
SIZES       = [1000, 10000, 100000, 1000000]
OPERATIONS  = ["insert", "search", "update", "delete", "iterate"]


# ── Load ──────────────────────────────────────────────────────────────────────
def load_stats(results_dir: Path) -> pd.DataFrame:
    path = results_dir / "descriptive_stats.csv"
    if not path.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {path}\nJalankan dulu 02_statistical_analysis.py")
    df = pd.read_csv(path)
    return df

def load_pairs(results_dir: Path) -> pd.DataFrame:
    path = results_dir / "pairwise_comparison.csv"
    if not path.exists():
        raise FileNotFoundError(f"Tidak ditemukan: {path}")
    return pd.read_csv(path)

def load_memory(results_dir: Path) -> pd.DataFrame:
    path = results_dir / "memory_footprint.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)

def load_effects(results_dir: Path) -> pd.DataFrame:
    path = results_dir / "effect_sizes.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


# ── Fig 1: Execution Time Heatmap ─────────────────────────────────────────────
def plot_execution_time(stats_df: pd.DataFrame, out_dir: Path):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Execution Time (ns/op) — ArrayList vs HashMap", fontsize=14, fontweight="bold")

    for ax, struct in zip(axes, ["ArrayList", "HashMap"]):
        pivot = stats_df[stats_df["structure"] == struct].pivot(
            index="operation", columns="dataset_size", values="mean_ns"
        )
        pivot.columns = SIZE_LABELS[:len(pivot.columns)]

        sns.heatmap(
            pivot, ax=ax, annot=True, fmt=".0f", cmap="YlOrRd",
            linewidths=0.5, cbar_kws={"label": "ns/op"},
        )
        ax.set_title(struct, fontsize=13, fontweight="bold",
                     color=COLORS[struct])
        ax.set_xlabel("Dataset Size")
        ax.set_ylabel("Operation")
        ax.tick_params(axis="x", rotation=0)

    plt.tight_layout()
    path = out_dir / "fig_execution_time.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  → {path}")


# ── Fig 2: Speedup Ratio ──────────────────────────────────────────────────────
def plot_speedup(pairs_df: pd.DataFrame, out_dir: Path):
    """Speedup = AL_mean / HM_mean. >1 berarti HashMap lebih cepat."""
    pairs_df = pairs_df.copy()
    pairs_df["speedup"] = pairs_df["AL_mean_ns"] / pairs_df["HM_mean_ns"]
    pairs_df["size_label"] = pairs_df["dataset_size"].map(
        dict(zip(SIZES, SIZE_LABELS))
    )

    fig, axes = plt.subplots(1, len(OPERATIONS), figsize=(16, 5), sharey=False)
    fig.suptitle("Speedup HashMap vs ArrayList (ratio > 1 = HashMap lebih cepat)",
                 fontsize=13, fontweight="bold")

    for ax, op in zip(axes, OPERATIONS):
        sub = pairs_df[pairs_df["operation"] == op].sort_values("dataset_size")
        colors = [COLORS["win"] if s > 1 else COLORS["lose"] for s in sub["speedup"]]
        bars = ax.bar(sub["size_label"], sub["speedup"], color=colors, edgecolor="white", width=0.6)
        ax.axhline(1.0, color="black", linewidth=1, linestyle="--", alpha=0.5)
        ax.set_title(op.capitalize(), fontweight="bold")
        ax.set_xlabel("Size")
        if op == OPERATIONS[0]:
            ax.set_ylabel("Speedup ratio")
        ax.tick_params(axis="x", rotation=30)

        # Label nilai
        for bar, val in zip(bars, sub["speedup"]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f"{val:.1f}x", ha="center", va="bottom", fontsize=9)

    legend = [
        mpatches.Patch(color=COLORS["win"],  label="HashMap lebih cepat"),
        mpatches.Patch(color=COLORS["lose"], label="ArrayList lebih cepat"),
    ]
    fig.legend(handles=legend, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.05))
    plt.tight_layout()
    path = out_dir / "fig_speedup_ratio.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  → {path}")


# ── Fig 3: Memory Footprint ───────────────────────────────────────────────────
def plot_memory(mem_df: pd.DataFrame, out_dir: Path):
    if mem_df is None:
        print("  [SKIP] memory_footprint.csv tidak ditemukan")
        return

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Memory Footprint — ArrayList vs HashMap", fontsize=13, fontweight="bold")

    # Panel kiri: deep bytes total
    ax = axes[0]
    for struct, color in [("ArrayList", COLORS["ArrayList"]), ("HashMap", COLORS["HashMap"])]:
        sub = mem_df[mem_df["data_structure"] == struct].sort_values("dataset_size")
        ax.plot(sub["dataset_size"], sub["deep_bytes"] / 1024**2,
                marker="o", label=struct, color=color, linewidth=2)
    ax.set_xscale("log")
    ax.set_xlabel("Dataset Size (log scale)")
    ax.set_ylabel("Memory (MB)")
    ax.set_title("Total Deep Size (MB)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel kanan: bytes per element
    ax = axes[1]
    pivot = mem_df.pivot(index="dataset_size", columns="data_structure",
                         values="bytes_per_element")
    pivot.plot(kind="bar", ax=ax,
               color=[COLORS["ArrayList"], COLORS["HashMap"]],
               edgecolor="white", width=0.7)
    ax.set_xlabel("Dataset Size")
    ax.set_ylabel("Bytes per Element")
    ax.set_title("Memory per Element (bytes)")
    ax.set_xticklabels(SIZE_LABELS[:len(pivot)], rotation=0)
    ax.legend(title="Structure")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    path = out_dir / "fig_memory_footprint.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  → {path}")


# ── Fig 4: Decision Matrix ────────────────────────────────────────────────────
def plot_decision_matrix(pairs_df: pd.DataFrame, eff_df: pd.DataFrame,
                         out_dir: Path) -> pd.DataFrame:
    """
    Decision matrix: untuk setiap operasi × ukuran,
    tampilkan rekomendasi + justifikasi.
    """
    matrix = []
    for op in OPERATIONS:
        for size in SIZES:
            p_row  = pairs_df[(pairs_df["operation"] == op) &
                               (pairs_df["dataset_size"] == size)]
            e_row  = eff_df[(eff_df["operation"] == op) &
                             (eff_df["dataset_size"] == size)] if eff_df is not None else None

            if len(p_row) == 0:
                rec = "N/A"
                justification = ""
                sig = False
                d = 0
            else:
                p_row = p_row.iloc[0]
                sig   = p_row["significant"]
                d     = e_row.iloc[0]["cohens_d"] if e_row is not None and len(e_row) > 0 else 0
                faster = p_row["faster"]
                diff_pct = abs(p_row["diff_pct"])

                if sig and d >= 0.5:
                    rec = faster
                    justification = f"{faster} {diff_pct:.0f}% lebih cepat (d={d:.2f})"
                elif sig:
                    rec = faster
                    justification = f"{faster} lebih cepat (d={d:.2f}, small effect)"
                else:
                    rec = "Either"
                    justification = f"Tidak ada perbedaan signifikan (p={p_row['p_bonferroni']:.3f})"

            matrix.append({
                "operation"   : op,
                "dataset_size": size,
                "recommended" : rec,
                "justification": justification,
                "significant" : sig,
                "cohens_d"    : d,
            })

    mat_df = pd.DataFrame(matrix)

    # Simpan CSV
    csv_path = out_dir / "decision_matrix.csv"
    mat_df.to_csv(csv_path, index=False)

    # Plot heatmap decision matrix
    pivot_rec = mat_df.pivot(index="operation", columns="dataset_size", values="recommended")
    pivot_d   = mat_df.pivot(index="operation", columns="dataset_size", values="cohens_d")

    # Encode: ArrayList=0, HashMap=1, Either=0.5
    encode = {"ArrayList": 0, "HashMap": 1, "Either": 0.5, "N/A": 0.5}
    pivot_enc = pivot_rec.replace(encode).astype(float)

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.suptitle("Decision Matrix — Pilih Struktur Data yang Tepat",
                 fontsize=13, fontweight="bold")

    cmap = plt.cm.get_cmap("RdYlGn", 3)
    im = ax.imshow(pivot_enc.values, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(SIZES)))
    ax.set_xticklabels(SIZE_LABELS)
    ax.set_yticks(range(len(OPERATIONS)))
    ax.set_yticklabels([op.capitalize() for op in pivot_rec.index])
    ax.set_xlabel("Dataset Size")
    ax.set_ylabel("Operation")

    # Anotasi tiap cell
    for i in range(len(pivot_rec.index)):
        for j in range(len(pivot_rec.columns)):
            rec = pivot_rec.values[i, j]
            d   = pivot_d.values[i, j]
            text = f"{rec}\nd={d:.2f}" if isinstance(d, float) else str(rec)
            color = "white" if rec == "HashMap" else "black"
            ax.text(j, i, text, ha="center", va="center",
                    fontsize=9, fontweight="bold", color=color)

    # Legend
    legend_handles = [
        mpatches.Patch(color=cmap(0.0), label="Gunakan ArrayList"),
        mpatches.Patch(color=cmap(0.5), label="Either (tidak signifikan)"),
        mpatches.Patch(color=cmap(1.0), label="Gunakan HashMap"),
    ]
    ax.legend(handles=legend_handles, loc="upper right",
              bbox_to_anchor=(1.35, 1), title="Rekomendasi")

    plt.tight_layout()
    path = out_dir / "fig_decision_matrix.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  → {path}")
    print(f"  → {csv_path}")

    return mat_df


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    results_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("results")

    print(f"\n{'='*55}")
    print(f"  VISUALISASI BENCHMARK")
    print(f"  Input dir: {results_dir}")
    print(f"{'='*55}\n")

    stats_df = load_stats(results_dir)
    pairs_df = load_pairs(results_dir)
    mem_df   = load_memory(results_dir)
    eff_df   = load_effects(results_dir)

    print("  Membuat visualisasi...")
    plot_execution_time(stats_df, results_dir)
    plot_speedup(pairs_df, results_dir)
    plot_memory(mem_df, results_dir)
    plot_decision_matrix(pairs_df, eff_df, results_dir)

    print(f"\n  Semua visualisasi tersimpan di: {results_dir}")
    print(f"  File yang dihasilkan:")
    for f in sorted(results_dir.glob("fig_*.png")):
        print(f"    {f.name}")
    print()


if __name__ == "__main__":
    main()
