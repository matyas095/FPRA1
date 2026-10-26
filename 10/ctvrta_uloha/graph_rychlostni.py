import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

from scipy.optimize import curve_fit

script_dir = Path(__file__).parent
data_dir = script_dir / "data" / "rychlostni"
output_dir = script_dir / "outputs"
subfolders = sorted(
    [f for f in data_dir.iterdir() if f.is_dir()], key=lambda f: f.name
)

x_err = 0.001015
y_err = 0.01155

firstGroup = np.load(rf"{data_dir}/group_1_data.npy", allow_pickle=True)
secondGroup = np.load(rf"{data_dir}/group_2_data.npy", allow_pickle=True)

x_vals = firstGroup[:, 1].astype(float)
y_vals = secondGroup[:, 1].astype(float)

def fit_rychlostni(t, Omega_0, delta, offset):
    return Omega_0 * t * np.exp(-delta * t) + offset

p0_rych = [1.0, 1.0, np.mean(y_vals[-10:])]

popt_rych, pcov_rych = curve_fit(fit_rychlostni, x_vals, y_vals, p0=p0_rych)
perr = np.sqrt(np.diag(pcov_rych))

phi_0_opt, delta_opt, offset_opt = popt_rych


print("--- Výsledky fitu ---")
print(f"Fázový posun (phi_0)          = {phi_0_opt:.4f} ± {perr[0]:.4f}")
print(f"Koeficient útlumu (delta)     = {delta_opt:.4f} ± {perr[1]:.4f}")
print(f"Offset                        = {offset_opt:.4f} ± {perr[2]:.4f}")
print("-" * 40)

t_smooth = np.linspace(x_vals.min(), x_vals.max() + 0.1, 1000)
y_fit = fit_rychlostni(t_smooth, *popt_rych)

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

plt.plot(
    t_smooth,
    y_fit,
    color="r",
    linestyle="-",
    linewidth=2,
    label=(
        "Fit: $\\Omega_0 te^{-\\delta t}$"
    ),
    zorder=2,
)

plt.xlabel("$t$ [s]", fontsize=11)
plt.ylabel(f"$\\varphi$ [rad]", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / f"04-rychlost.svg"
plt.savefig(svg_name, format="svg")

plt.close()
