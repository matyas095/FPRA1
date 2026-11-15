import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path
import sys

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# Vstupní data
rychlosti_v = np.array([
    0.24450000000, 0.30740000000, 0.45680000000, 0.56730000000, 0.57540000000, 0.76330000000
]) # m/s
absolutni_chyby_v = np.array([
    0.00788845852, 0.00792772911, 0.00549100274, 0.00802226070, 0.01692086155, 0.01544959546
]) # m/s

v_m1 = rychlosti_v[0::2]
err_m1 = absolutni_chyby_v[0::2]

v_m2 = rychlosti_v[1::2]
err_m2 = absolutni_chyby_v[1::2]

comma_formatter = FuncFormatter(lambda x, pos: f"{x:.3f}".replace(".", ","))

# ========================
#  Absolutní chyba
# ========================
plt.figure(figsize=(9, 5))

plt.errorbar(
    v_m1, err_m1, xerr=err_m1, yerr=0,
    fmt="o", color="blue", ecolor="lightblue", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_1$", zorder=2
)

plt.errorbar(
    v_m2, err_m2, xerr=err_m2, yerr=0,
    fmt="s", color="red", ecolor="lightcoral", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_2$", zorder=2
)

plt.xlabel(r"$v$ [m/s]", fontsize=11)
plt.ylabel(r"$\sigma_{v}$ [m/s]", fontsize=11)

plt.gca().xaxis.set_major_formatter(comma_formatter)
plt.gca().yaxis.set_major_formatter(comma_formatter)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "abs_rychlosti_3.svg"
plt.savefig(svg_name, format="svg")
plt.close()

# ========================
#  Relativní chyby
# ========================
rel_m1 = err_m1 / v_m1 * 100
rel_m2 = err_m2 / v_m2 * 100

plt.figure(figsize=(9, 5))

plt.errorbar(
    v_m1, rel_m1, xerr=err_m1, yerr=0,
    fmt="o", color="blue", ecolor="lightblue", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_1$", zorder=2
)

plt.errorbar(
    v_m2, rel_m2, xerr=err_m2, yerr=0,
    fmt="s", color="red", ecolor="lightcoral", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_2$", zorder=2
)

plt.xlabel(r"$v$ [m/s]", fontsize=11)
plt.ylabel(r"$\delta_{v}$ [%]", fontsize=11)

plt.gca().xaxis.set_major_formatter(comma_formatter)
plt.gca().yaxis.set_major_formatter(comma_formatter)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "rel_rychlosti_3.svg"
plt.savefig(svg_name, format="svg")
plt.close()