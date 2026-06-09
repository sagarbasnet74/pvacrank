"""Benchmarking utilities."""
from typing import Dict
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

def benchmark_ranker(ranked_df, labels_df, id_col="ID", label_col="label", score_col="composite_score"):
    merged = ranked_df.merge(labels_df[[id_col, label_col]], on=id_col, how="inner")
    if len(merged) == 0:
        raise ValueError(f"No matching IDs. Check '{id_col}' exists in both.")
    y_true, y_scores = merged[label_col].values, merged[score_col].values
    if len(np.unique(y_true)) < 2:
        return {"auroc": np.nan, "auprc": np.nan, "top10_recall": np.nan, "top20_recall": np.nan, "top50_recall": np.nan}
    auroc, auprc = roc_auc_score(y_true, y_scores), average_precision_score(y_true, y_scores)
    n_pos = int(y_true.sum())
    sorted_labels = y_true[np.argsort(-y_scores)]
    return {
        "auroc": float(auroc), "auprc": float(auprc),
        "top10_recall": float(sorted_labels[:10].sum() / n_pos) if n_pos else 0.0,
        "top20_recall": float(sorted_labels[:20].sum() / n_pos) if n_pos else 0.0,
        "top50_recall": float(sorted_labels[:50].sum() / n_pos) if n_pos else 0.0,
    }
