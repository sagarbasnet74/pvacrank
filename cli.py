"""CLI for pVACrank."""
import argparse
import sys
import json
from pathlib import Path
import pandas as pd
from .ranker import CompositeRanker
from .weights import get_preset, list_presets
from .benchmark import benchmark_ranker

def main():
    parser = argparse.ArgumentParser(description="pVACrank: Composite re-ranking for pVACseq")
    parser.add_argument("input", help="Path to pVACseq aggregated.tsv")
    parser.add_argument("-o", "--output", required=True, help="Output path for re-ranked TSV")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--preset", choices=list_presets())
    g.add_argument("--weights", type=str, help="Path to JSON weights file")
    parser.add_argument("--benchmark", type=str, help="Ground-truth labels TSV (columns: ID, label)")
    parser.add_argument("--id-col", default="ID", help="ID column name for benchmarking")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t")
    print(f"Loaded {len(df)} rows")

    weights = get_preset(args.preset) if args.preset else json.load(open(args.weights))
    ranker = CompositeRanker(weights=weights)
    ranked = ranker.rank(df)
    print(f"Best score: {ranked['composite_score'].max():.4f}")

    if args.verbose:
        for feat in ranker.weights:
            norm_col = f"{feat}_norm"
            if norm_col in ranked.columns:
                print(f"  {feat}: {(ranked[norm_col] * ranker.weights[feat]).mean():.4f}")

    if args.benchmark:
        labels_df = pd.read_csv(args.benchmark, sep="\t")
        metrics = benchmark_ranker(ranked, labels_df, id_col=args.id_col)
        print(f"\nAUROC: {metrics['auroc']:.4f}")
        print(f"AUPRC: {metrics['auprc']:.4f}")
        print(f"Top-10 Recall: {metrics['top10_recall']:.4f}")
        print(f"Top-20 Recall: {metrics['top20_recall']:.4f}")
        print(f"Top-50 Recall: {metrics['top50_recall']:.4f}")

    ranked.to_csv(args.output, sep="\t", index=False)
    print(f"Wrote to {args.output}")

if __name__ == "__main__":
    main()
