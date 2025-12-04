### This .py provides data plotting functions
###

import matplotlib.pyplot as plt

def bar_plot (label: list[str],
              value: list[int],
              id_list: list[str],
              plot_type: str,
              ):
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(label, value, color='SteelBlue')
    # Add numbers on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Count")
    plt.title(f"{id_list[0]}_{id_list[1]}_{id_list[2]}_{plot_type}")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(f"{id_list[1]}_{id_list[2]}_{plot_type}.png", dpi=300, bbox_inches="tight")

    return True