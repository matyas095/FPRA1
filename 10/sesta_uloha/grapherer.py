import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

from scipy.optimize import curve_fit

x_err = 0.001015
y_err = 0.01155

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"
subfolders = sorted(
    [f for f in data_dir.iterdir() if f.is_dir()], key=lambda f: f.name
)
file = np.load(f"data/1/combined_data.npy", allow_pickle=True)
for index, group in enumerate(file, start=1):
    firstGroup, secondGroup = group

    x_vals = firstGroup[:, 1].astype(float)
    y_vals = secondGroup[:, 1].astype(float)

    plt.figure(figsize=(9, 5))

    random_color = np.random.rand(3)

    plt.errorbar(
        x_vals,
        y_vals,
        xerr=x_err,
        yerr=y_err,
        fmt="o",
        color=random_color,
        ecolor="gray",
        elinewidth=1,
        capsize=2,
        markersize=5,
        label=f"Naměřená data s chybami",
        zorder=1,
    )

    plt.xlabel("$t$ [s]", fontsize=11)
    plt.ylabel(r"$\varphi$ [rad]", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()

    svg_name = output_dir / "bez_tlum" / f"{index}.svg"
    plt.savefig(svg_name, format="svg")

    plt.close()