"""Streamlit web app for pVACrank interactive exploration."""

import sys
from pathlib import Path

# Add repo root to path for absolute imports
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ranker import CompositeRanker
from weights import PRESETS, get_preset, list_presets
from benchmark import benchmark_ranker

st.set_page_config(page_title="pVACrank Explorer", layout="wide")

st.title("pVACrank: Composite Immunogenicity Ranker")
st.markdown("Interactive exploration of neoantigen ranking strategies for pVACtools")

# Sidebar
st.sidebar.header("Data Source")

# Option to auto-load example data
auto_load = st.sidebar.checkbox("Auto-load HCC1395 example data", value=True)

st.sidebar.header("Upload Custom Data")
uploaded_file = st.sidebar.file_uploader("Or upload your own aggregated.tsv", type=["tsv", "csv"])

# Determine data source
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep="\t")
    st.success(f"Loaded {len(df)} variants from uploaded file")
elif auto_load:
    example_path = "pvacseq_example_data/pvacseq_example_data/results/MHC_Class_I/HCC1395_TUMOR_DNA.MHC_I.all_epitopes.aggregated.tsv"
    if Path(example_path).exists():
        df = pd.read_csv(example_path, sep="\t")
        st.success(f"Auto-loaded {len(df)} variants from HCC1395 example data")
    else:
        st.error(f"Example data not found at {example_path}")
        st.info("Please upload a file or check the example data path")
        df = None
else:
    st.info("Check 'Auto-load example data' or upload a file")
    df = None

# Only proceed if we have data
if df is not None:
    st.sidebar.header("Weight Configuration")
    preset_choice = st.sidebar.selectbox("Choose Preset", list_presets())

    # Custom weights expander
    with st.sidebar.expander("Or define custom weights"):
        custom_weights = {}
        for feat in CompositeRanker.DEFAULT_FEATURES:
            default_val = get_preset(preset_choice).get(feat, 0.1)
            custom_weights[feat] = st.slider(feat, 0.0, 1.0, default_val, 0.05)
        use_custom = st.checkbox("Use custom weights")

    st.sidebar.header("Benchmark")
    labels_file = st.sidebar.file_uploader("Upload labels (optional)", type=["tsv", "csv"])

    # Run ranking
    if use_custom:
        weights = custom_weights
        st.info("Using custom weights")
    else:
        weights = get_preset(preset_choice)
        st.info(f"Using preset: **{preset_choice}**")

    ranker = CompositeRanker(weights=weights)
    ranked = ranker.rank(df)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Ranked Results", "Feature Analysis", "Benchmark", "Weights"])

    with tab1:
        st.subheader("Top Ranked Neoantigens")
        display_cols = ["ID", "Gene", "AA Change", "composite_score", "composite_rank",
                        "IC50 MT", "IM %ile MT", "Pres %ile MT", "RNA Expr", "DNA VAF", "Tier"]
        available_cols = [c for c in display_cols if c in ranked.columns]
        st.dataframe(ranked[available_cols].head(20), width="stretch")

        # Score distribution
        st.subheader("Composite Score Distribution")
        fig, ax = plt.subplots()
        ax.hist(ranked["composite_score"], bins=30, color="steelblue", edgecolor="black")
        ax.set_xlabel("Composite Score")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # Download
        csv = ranked.to_csv(sep="\t", index=False)
        st.download_button("Download Ranked TSV", csv, "ranked_results.tsv", "text/tab-separated-values")

    with tab2:
        st.subheader("Feature Importance")
        importance = ranker.get_feature_importance(ranked)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            features = list(importance.keys())
            values = list(importance.values())
            ax.barh(features, values, color="coral")
            ax.set_xlabel("Average Contribution")
            st.pyplot(fig)
        with col2:
            st.write("**Feature Contributions**")
            for feat, contrib in sorted(importance.items(), key=lambda x: -x[1]):
                st.write(f"{feat}: {contrib:.4f}")

    with tab3:
        if labels_file is not None:
            labels_df = pd.read_csv(labels_file, sep="\t")
            try:
                metrics = benchmark_ranker(ranked, labels_df)

                col1, col2, col3 = st.columns(3)
                col1.metric("AUROC", f"{metrics['auroc']:.4f}")
                col2.metric("AUPRC", f"{metrics['auprc']:.4f}")
                col3.metric("Top-50 Recall", f"{metrics['top50_recall']:.4f}")

                st.subheader("Detailed Metrics")
                metrics_df = pd.DataFrame([metrics]).T
                metrics_df.columns = ["Value"]
                st.dataframe(metrics_df, width="stretch")
            except Exception as e:
                st.error(f"Benchmark failed: {e}")
        else:
            st.info("Upload a labels file to see benchmark metrics")

    with tab4:
        st.subheader("Current Weights")
        weights_df = pd.DataFrame([weights]).T
        weights_df.columns = ["Weight"]
        st.dataframe(weights_df, width="stretch")

        st.subheader("Preset Comparison")
        preset_df = pd.DataFrame(PRESETS).T
        st.dataframe(preset_df, width="stretch")

        st.subheader("Preset Weights Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(preset_df.values, cmap="YlOrRd", aspect="auto")
        ax.set_xticks(np.arange(len(preset_df.columns)))
        ax.set_yticks(np.arange(len(preset_df.index)))
        ax.set_xticklabels(preset_df.columns, rotation=45, ha="right")
        ax.set_yticklabels(preset_df.index)
        fig.colorbar(im, ax=ax)
        st.pyplot(fig)

else:
    st.info("Waiting for data... Check 'Auto-load example data' or upload a file")

    st.markdown("""
    ### What is pVACrank?

    pVACrank is a composite immunogenicity ranker for pVACtools that allows you to:

    1. **Combine multiple features** into a unified ranking score
    2. **Use predefined presets** optimized for different scenarios
    3. **Define custom weights** for your specific research question
    4. **Benchmark** against ground-truth immunogenicity labels

    ### Presets

    | Preset | Focus | Best For |
    |--------|-------|----------|
    | balanced | Equal weights | General screening |
    | binding-heavy | MHC binding | Strong binder prioritization |
    | immunogenicity-heavy | T-cell recognition | Immunotherapy design |
    | presentation-heavy | Antigen processing | Vaccine candidates |
    | expression-heavy | Tumor abundance | Highly expressed variants |
    | binding-only | Baseline | Comparison with default pVACseq |
    """)
