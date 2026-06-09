"""Core composite scoring logic for pVACrank."""
import pandas as pd
import numpy as np
from typing import Dict, Optional
import json

class CompositeRanker:
    DEFAULT_FEATURES = {
        "IC50 MT": {"invert": True},
        "%ile MT": {"invert": True},
        "IC50 %ile MT": {"invert": True},
        "IM %ile MT": {"invert": True},
        "Pres %ile MT": {"invert": True},
        "RNA Expr": {"invert": False},
        "RNA VAF": {"invert": False},
        "DNA VAF": {"invert": False},
        "Allele Expr": {"invert": False},
    }

    def __init__(self, weights=None):
        self.weights = weights or self._equal_weights()
        self._validate_weights()

    def _equal_weights(self):
        n = len(self.DEFAULT_FEATURES)
        return {k: round(1.0/n, 3) for k in self.DEFAULT_FEATURES}

    def _validate_weights(self):
        for feat in self.weights:
            if feat not in self.DEFAULT_FEATURES:
                raise ValueError(f"Unknown feature: '{feat}'. Available: {list(self.DEFAULT_FEATURES.keys())}")

    def _normalize(self, series, invert=False):
        s = pd.to_numeric(series, errors="coerce").copy()
        if s.isna().all():
            return pd.Series(0.0, index=s.index)
        min_val, max_val = s.min(), s.max()
        if max_val == min_val:
            normalized = pd.Series(0.5, index=s.index)
        else:
            normalized = (s - min_val) / (max_val - min_val)
        if invert:
            normalized = 1.0 - normalized
        return normalized.fillna(0.0)

    def rank(self, df):
        df = df.copy()
        composite = pd.Series(0.0, index=df.index)
        for feature, weight in self.weights.items():
            if feature not in df.columns:
                raise ValueError(f"Feature '{feature}' not found. Available: {list(df.columns)}")
            invert = self.DEFAULT_FEATURES[feature]["invert"]
            normalized = self._normalize(df[feature], invert=invert)
            df[f"{feature}_norm"] = normalized
            composite += weight * normalized
        df["composite_score"] = composite
        df["composite_rank"] = df["composite_score"].rank(ascending=False, method="min").astype(int)
        return df.sort_values("composite_score", ascending=False).reset_index(drop=True)

    def to_dict(self):
        return {"weights": self.weights}

    @classmethod
    def from_dict(cls, config):
        return cls(weights=config.get("weights"))

    @classmethod
    def from_json(cls, path):
        with open(path) as f:
            return cls.from_dict(json.load(f))


    def get_feature_importance(self, df):
        """Compute per-feature contribution to composite scores."""
        importance = {}
        for feat, weight in self.weights.items():
            norm_col = f"{feat}_norm"
            if norm_col in df.columns:
                importance[feat] = (df[norm_col] * weight).mean()
        return importance
