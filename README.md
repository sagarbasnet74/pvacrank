# pVACrank

**Composite Immunogenicity Ranker for pVACtools**

A configurable post-processing extension that adds weighted composite scoring and re-ranking to pVACseq neoantigen predictions.

---

## Overview

pVACtools v7.0 provides powerful neoantigen prediction capabilities through models such as PRIME, ImmuScope, and MixMHCpred. However, candidate ranking is fixed and may not align with specific research or clinical objectives.

**pVACrank** addresses this limitation by enabling customizable composite scoring and re-ranking of pVACseq predictions.

### Features

* Combine 9 biologically relevant features into a unified composite score
* Choose from 6 predefined ranking presets
* Define custom feature weights for specific research questions
* Benchmark rankings against ground-truth immunogenicity labels
* Generate publication-quality visualizations
* Explore results interactively through a Streamlit web application
* Operates entirely downstream of pVACtools with zero modifications to the core codebase

---

## Key Result

| Preset                  | AUROC  | Improvement vs Baseline |
| ----------------------- | ------ | ----------------------- |
| immunogenicity-heavy    | 0.8564 | +0.19                   |
| binding-only (baseline) | 0.6686 | —                       |

*Benchmarked on HCC1395 cell line data using synthetic immunogenicity labels.*

---

## Features Used for Ranking

| Feature            | Column       | Direction        | Biological Meaning                             |
| ------------------ | ------------ | ---------------- | ---------------------------------------------- |
| IC50 MT            | IC50 MT      | Lower is better  | Mutant peptide binding affinity                |
| Binding Percentile | %ile MT      | Lower is better  | Relative MHC binding strength                  |
| IC50 Percentile    | IC50 %ile MT | Lower is better  | Normalized IC50 rank                           |
| Immunogenicity     | IM %ile MT   | Lower is better  | T-cell recognition potential                   |
| Presentation       | Pres %ile MT | Lower is better  | Antigen processing and presentation efficiency |
| Gene Expression    | RNA Expr     | Higher is better | Transcript abundance                           |
| RNA VAF            | RNA VAF      | Higher is better | Variant allele fraction in RNA                 |
| DNA VAF            | DNA VAF      | Higher is better | Variant allele fraction in DNA                 |
| Allele Expression  | Allele Expr  | Higher is better | Allele-specific expression level               |

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/sagarbasnet74/pvacrank.git
cd pvacrank
```

### Install Package

```bash
pip install -e .
```

---

## Quick Start

### 1. Rank Neoantigens Using a Preset

```bash
pvacseq-rank aggregated.tsv \
    --preset immunogenicity-heavy \
    -o ranked.tsv
```

### 2. Benchmark Against Ground-Truth Labels

```bash
pvacseq-rank aggregated.tsv \
    --preset balanced \
    --benchmark labels.tsv \
    --id-col ID \
    -o ranked.tsv
```

### 3. Run Full Benchmark Suite

```bash
pvacseq-benchmark aggregated.tsv \
    labels.tsv \
    --output-dir results/
```

### 4. Launch Interactive Web Application

```bash
streamlit run pvacrank/app.py
```

---

## Presets

| Preset               | Focus                    | Recommended Use Case                          |
| -------------------- | ------------------------ | --------------------------------------------- |
| balanced             | Equal weighting          | General neoantigen screening                  |
| binding-heavy        | 70% binding features     | Strong MHC binder prioritization              |
| immunogenicity-heavy | 35% immunogenicity score | Immunotherapy candidate selection             |
| presentation-heavy   | 35% presentation score   | Vaccine target prioritization                 |
| expression-heavy     | 70% expression features  | Highly expressed tumor variants               |
| binding-only         | 100% binding features    | Baseline ranking (similar to default pVACseq) |

---

## Benchmark Results

### HCC1395 Cell Line (Synthetic Labels)

| Preset               | AUROC  | AUPRC  | Top-10 Recall | Top-20 Recall | Top-50 Recall |
| -------------------- | ------ | ------ | ------------- | ------------- | ------------- |
| immunogenicity-heavy | 0.8564 | 0.3911 | 0.2500        | 0.2500        | 0.5500        |
| presentation-heavy   | 0.8331 | 0.3890 | 0.2500        | 0.2500        | 0.5500        |
| balanced             | 0.8330 | 0.3044 | 0.3000        | 0.3000        | 0.4500        |
| expression-heavy     | 0.8173 | 0.2548 | 0.2000        | 0.3500        | 0.3500        |
| binding-heavy        | 0.8115 | 0.2886 | 0.2500        | 0.2500        | 0.5500        |
| binding-only         | 0.6686 | 0.1038 | 0.1000        | 0.1000        | 0.2000        |

### Key Finding

The **immunogenicity-heavy** preset improves AUROC by **0.19** compared to the traditional binding-only ranking approach, demonstrating the value of incorporating immunogenicity and presentation features into neoantigen prioritization.

---

## Methodology

### Ranking Workflow

```text
pVACseq aggregated.tsv
        |
        v
+------------------+
| CompositeRanker  |
+------------------+
        |
        |- Min-max normalize features to [0,1]
        |- Invert "lower is better" metrics
        |- Apply configurable feature weights
        |- Compute composite score
        |
        v
Re-ranked TSV Output
        |
        |- composite_score
        |- composite_rank
        |- normalized feature values
```

### Design Principle

pVACrank is intentionally designed as a downstream analysis tool.

* No modifications to pVACtools source code
* Compatible with existing pVACseq workflows
* Operates directly on `aggregated.tsv` outputs
* Easily integrates into current neoantigen pipelines

---

## Project Structure

```text
pvacrank/
├── ranker.py            # Composite scoring engine
├── weights.py           # Preset weight configurations
├── cli.py               # Command-line interface
├── benchmark.py         # AUROC/AUPRC evaluation
├── benchmark_all.py     # Full benchmarking workflow
├── visualize.py         # Plotting utilities
└── app.py               # Streamlit web application

tests/
└── test_pvacrank.py     # Unit tests

data/
└── synthetic_labels.tsv # Example labels

figures/
└── preset_comparison.png

README.md
setup.py
LICENSE
```

---

## Testing

Run the test suite:

```bash
python -m unittest tests.test_pvacrank
```

---

## License

This project is distributed under the MIT License.

See the `LICENSE` file for details.

---

## Citation

If you use pVACrank in your research, please cite:

```text
Basnet, S. pVACrank: Composite Immunogenicity Ranker for pVACtools.
GitHub Repository: https://github.com/sagarbasnet74/pvacrank
```
