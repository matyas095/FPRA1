import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
import numpy as np
from sympy.printing import latex

script_dir = Path(__file__).parent
data_dir = script_dir / "inputs" / "1"
output_dir = script_dir / "outputs"
output_dir.mkdir(exist_ok=True)

x_err = 0.5
y_err = 0.1

firstGroup = np.load(rf"{data_dir}/group_1_data.npy", allow_pickle=True)
secondGroup = np.load(rf"{data_dir}/group_2_data.npy", allow_pickle=True)

x_vals = firstGroup[:, 1].astype(float)
y_vals = secondGroup[:, 1].astype(float)
y_vals = y_vals + 273.15

# --- 1. Split raw data into THREE parts using two thresholds ---
split_1 = 59880
split_2 = 61000
print(f"Time range: min = {x_vals.min()}, max = {x_vals.max()}")

mask_1 = x_vals <= split_1
mask_2 = (x_vals > split_1) & (x_vals <= split_2)
mask_3 = x_vals > split_2

x_vals_1, y_vals_1 = x_vals[mask_1], y_vals[mask_1]
x_vals_2, y_vals_2 = x_vals[mask_2], y_vals[mask_2]
x_vals_3, y_vals_3 = x_vals[mask_3], y_vals[mask_3]

# --- 2. Perform separate linear fits only for Part 1 and Part 3 ---
(slope1, intercept1), pcov1 = np.polyfit(x_vals_1, y_vals_1, 1, cov=True)
slope1_err, intercept1_err = np.sqrt(np.diag(pcov1))

(slope3, intercept3), pcov3 = np.polyfit(x_vals_3, y_vals_3, 1, cov=True)
slope3_err, intercept3_err = np.sqrt(np.diag(pcov3))

print("--- Výsledky 1. lineárního fitu ---")
print(f"a1 = {slope1:.6f} ± {slope1_err:.6f}")
print(f"b1 = {intercept1:.1f} ± {intercept1_err:.1f}")
print("-" * 40)
print("--- Výsledky 2. lineárního fitu ---")
print(f"a2 = {slope3:.6f} ± {slope3_err:.6f}")
print(f"b2 = {intercept3:.1f} ± {intercept3_err:.1f}")
print("-" * 40)

# --- 3. Generate smooth lines for Part 1 and Part 3 ---
t_smooth_1 = np.linspace(x_vals_1.min(), x_vals_1.max(), 300)
y_fit_1 = slope1 * t_smooth_1 + intercept1

t_smooth_3 = np.linspace(x_vals_3.min(), x_vals_3.max(), 300)
y_fit_3 = slope3 * t_smooth_3 + intercept3

# --- 4. Plotting ---
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
    markersize=2,
    label="Naměřená data s chybami",
    zorder=1,
)

plt.plot(
    t_smooth_1,
    y_fit_1,
    color="r",
    linestyle="-",
    linewidth=2,
    label=f"Fit 1: $y = a_1 \\cdot x + b_1$",
    zorder=2,
)

plt.plot(
    t_smooth_3,
    y_fit_3,
    color="b",
    linestyle="-",
    linewidth=2,
    label=f"Fit 3: $y = a_2 \\cdot x + b_2$",
    zorder=2,
)

plt.xlabel("$t$ [s]", fontsize=11)
plt.ylabel("$T$ [K]", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=9)
plt.tight_layout()

svg_name = output_dir / "01-tepelna-kapacita_1.png"
plt.savefig(svg_name, format="png")
plt.close()