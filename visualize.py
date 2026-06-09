"""Visualization utilities for pVACrank."""
import matplotlib.pyplot as plt
import numpy as np

def plot_preset_comparison_bar(auroc_dict, auprc_dict, output_path='preset_comparison.png'):
    presets = list(auroc_dict.keys())
    x = np.arange(len(presets))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, [auroc_dict[p] for p in presets], width, label='AUROC', color='steelblue', edgecolor='black')
    ax.bar(x + width/2, [auprc_dict[p] for p in presets], width, label='AUPRC', color='coral', edgecolor='black')
    ax.set_xlabel('Preset', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('pVACrank Preset Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(presets, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim([0, 1.0])
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()
