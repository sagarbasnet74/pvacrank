"""Full benchmark suite with figure generation."""
import pandas as pd
from pathlib import Path
from .ranker import CompositeRanker
from .weights import get_preset, list_presets
from .benchmark import benchmark_ranker
from .visualize import plot_preset_comparison_bar

def run_full_benchmark(input_tsv, labels_tsv, output_dir='benchmark_results'):
    Path(output_dir).mkdir(exist_ok=True)
    df = pd.read_csv(input_tsv, sep="\t")
    labels_df = pd.read_csv(labels_tsv, sep="\t")
    results = {}
    for preset in list_presets():
        print(f"\n=== {preset} ===")
        ranker = CompositeRanker(weights=get_preset(preset))
        ranked = ranker.rank(df)
        metrics = benchmark_ranker(ranked, labels_df)
        results[preset] = metrics
        print(f"  AUROC: {metrics['auroc']:.4f}  AUPRC: {metrics['auprc']:.4f}")
    pd.DataFrame(results).T.to_csv(f"{output_dir}/metrics.csv")
    plot_preset_comparison_bar(
        {p: r['auroc'] for p, r in results.items()},
        {p: r['auprc'] for p, r in results.items()},
        f"{output_dir}/comparison.png"
    )
    print(f"\nAll results in {output_dir}/")
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('labels')
    parser.add_argument('--output-dir', default='benchmark_results')
    args = parser.parse_args()
    run_full_benchmark(args.input, args.labels, args.output_dir)
