"""Preset weight configurations."""
PRESETS = {
    "balanced": {
        "IC50 MT": 0.111, "%ile MT": 0.111, "IC50 %ile MT": 0.111,
        "IM %ile MT": 0.111, "Pres %ile MT": 0.111, "RNA Expr": 0.111,
        "RNA VAF": 0.111, "DNA VAF": 0.111, "Allele Expr": 0.112,
    },
    "binding-heavy": {
        "IC50 MT": 0.30, "%ile MT": 0.20, "IC50 %ile MT": 0.20,
        "IM %ile MT": 0.05, "Pres %ile MT": 0.05, "RNA Expr": 0.05,
        "RNA VAF": 0.05, "DNA VAF": 0.05, "Allele Expr": 0.05,
    },
    "immunogenicity-heavy": {
        "IC50 MT": 0.10, "%ile MT": 0.10, "IC50 %ile MT": 0.10,
        "IM %ile MT": 0.35, "Pres %ile MT": 0.15, "RNA Expr": 0.05,
        "RNA VAF": 0.05, "DNA VAF": 0.05, "Allele Expr": 0.05,
    },
    "presentation-heavy": {
        "IC50 MT": 0.10, "%ile MT": 0.10, "IC50 %ile MT": 0.10,
        "IM %ile MT": 0.10, "Pres %ile MT": 0.35, "RNA Expr": 0.05,
        "RNA VAF": 0.05, "DNA VAF": 0.05, "Allele Expr": 0.10,
    },
    "expression-heavy": {
        "IC50 MT": 0.05, "%ile MT": 0.05, "IC50 %ile MT": 0.05,
        "IM %ile MT": 0.05, "Pres %ile MT": 0.05, "RNA Expr": 0.25,
        "RNA VAF": 0.20, "DNA VAF": 0.20, "Allele Expr": 0.20,
    },
    "binding-only": {
        "IC50 MT": 0.50, "%ile MT": 0.30, "IC50 %ile MT": 0.20,
        "IM %ile MT": 0.0, "Pres %ile MT": 0.0, "RNA Expr": 0.0,
        "RNA VAF": 0.0, "DNA VAF": 0.0, "Allele Expr": 0.0,
    },
}

def list_presets():
    return list(PRESETS.keys())

def get_preset(name):
    if name not in PRESETS:
        raise ValueError(f"Unknown preset '{name}'. Available: {list_presets()}")
    return PRESETS[name].copy()
