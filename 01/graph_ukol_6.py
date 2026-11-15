import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.optimize import curve_fit
from pathlib import Path
import sys

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# ACTUAL SCRIPTS
from extr.funcs.rounder import round_val_err
from extr.data.colors import TextColor

# Vstupní data
p = np.array([
    76, 64, 142, 119, 180, 160
]) # g * m * s^{-1}
p_chyba = np.array([
    3, 2, 2, 2, 10, 4
]) # g * m * s^{-1}
p_m1 = p[0::2]
p_chyba_m1 = p_chyba[0::2]
p_m2 = p[1::2]
p_chyba_m2 = p_chyba[1::2]

p_carka = np.array([
    60, 73, 129, 130, 170, 140
]) # g * m * s^{-1}
p_carka_chyba = np.array([
    10, 4, 2, 10, 10, 10
]) # g * m * s^{-1}
p_carka_m1 = p_carka[0::2]
p_carka_chyba_m1 = p_carka_chyba[0::2]
p_carka_m2 = p_carka[1::2]
p_carka_chyba_m2 = p_carka_chyba[1::2]




E = np.array([
    9, 10, 32, 34, 52, 61
]) # mJ
E_chyba = np.array([
    2, 1, 1, 1, 4, 3
]) # mJ
E_m1 = E[0::2]
E_chyba_m1 = E_chyba[0::2]
E_m2 = E[1::2]
E_chyba_m2 = E_chyba[1::2]

E_carka = np.array([
    7, 7, 26, 22, 42, 27
]) # mJ
E_carka_chyba = np.array([
    4, 1, 1, 3, 3, 4
]) # mJ
E_carka_m1 = E_carka[0::2]
E_carka_chyba_m1 = E_carka_chyba[0::2]
E_carka_m2 = E_carka[1::2]
E_carka_chyba_m2 = E_carka_chyba[1::2]


comma_formatter = FuncFormatter(lambda x, pos: f"{x:.1f}".replace(".", ","))

# ========================
#  Hybnosti
# ========================
plt.figure(figsize=(9, 5))

plt.errorbar(
    p_m1, p_carka_m1, xerr=p_chyba_m1, yerr=p_carka_chyba_m1,
    fmt="o", color="blue", ecolor="lightblue", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_1$", zorder=2
)

plt.errorbar(
    p_m2, p_carka_m2, xerr=p_chyba_m2, yerr=p_carka_chyba_m2,
    fmt="s", color="red", ecolor="lightcoral", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_2$", zorder=2
)

max_val = np.max(np.concatenate((p, p_carka)))
print(max_val)
x_vals = np.linspace(0, max_val * 1.1, 1000)

plt.plot(
    x_vals,
    x_vals,
    color="green",
    label=fr"Ideální případ $p'=p\,(\Delta p = 0)$",
)


plt.xlabel(r"$p$ [$\mathrm{g\cdot m\cdot s^{-1}}$]", fontsize=11)
plt.ylabel(r"$p'$ [$\mathrm{g\cdot m\cdot s^{-1}}$]", fontsize=11)

# plt.gca().xaxis.set_major_formatter(comma_formatter)
# plt.gca().yaxis.set_major_formatter(comma_formatter)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "hybnost_6.svg"
plt.savefig(svg_name, format="svg")
plt.close()

# ========================
#  KInetické energie
# ========================
plt.figure(figsize=(9, 5))

plt.errorbar(
    E_m1, E_carka_m1, xerr=E_chyba_m1, yerr=E_carka_chyba_m1,
    fmt="o", color="blue", ecolor="lightblue", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_1$", zorder=2
)

plt.errorbar(
    E_m2, E_carka_m2, xerr=E_chyba_m2, yerr=E_carka_chyba_m2,
    fmt="s", color="red", ecolor="lightcoral", elinewidth=1,
    capsize=2, markersize=5, label="Konfigurace $m_2$", zorder=2
)

max_val = np.max(np.concatenate((E, E_carka)))
print(max_val)
x_vals = np.linspace(0, max_val * 1.1, 1000)

plt.plot(
    x_vals,
    x_vals,
    color="green",
    label=fr"Ideální případ $T'=T\,(\Delta T = 0)$",
)


plt.xlabel(r"$T$ [$\mathrm{mJ}$]", fontsize=11)
plt.ylabel(r"$T'$ [$\mathrm{mJ}$]", fontsize=11)

# plt.gca().xaxis.set_major_formatter(comma_formatter)
# plt.gca().yaxis.set_major_formatter(comma_formatter)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "kineticka_energie_6.svg"
plt.savefig(svg_name, format="svg")
plt.close()


# ========================
#  Proložení hybností
# ========================
p_int = np.array([
    0.07330, 0.17557, 0.22616
]) * 1000 # N ⋅ s -> g ⋅ m ⋅ s⁻¹
p_int_chyby = np.array([
    0.003444209714, 0.01037216949, 0.004543498407
]) * 1000 # N ⋅ s -> g ⋅ m ⋅ s⁻¹

p_rych = np.array([
    70.97112, 128.5474608, 171.1607238
]) # g ⋅ m ⋅ s⁻¹
p_rych_chyby = np.array([
    1.740891755, 2.122273655, 4.290779864
]) # g ⋅ m ⋅ s⁻¹

labels = ["Konfigurace první startovací rychlost", "Konfigurace druhá startovací rychlost", "Konfigurace třetí startovací rychlost"]
colors = [["o", "blue"], ["s", "red"], ["p", "green"]]


plt.figure(figsize=(9, 5))

for i, (pint, pinterr, prych, prycherr) in enumerate(zip(p_int, p_int_chyby, p_rych, p_rych_chyby)):
    plt.errorbar(
        prych, pint, xerr=prycherr, yerr=pinterr,
        fmt=colors[i][0], color=colors[i][1], ecolor="lightblue", elinewidth=1,
        capsize=2, markersize=5, label=labels[i], zorder=2
    )

# plt.errorbar(
#     p_rych[0], p_int[0], xerr=E_chyba_m1, yerr=p_int_chyby[0],
#     fmt="o", color="blue", ecolor="lightblue", elinewidth=1,
#     capsize=2, markersize=5, label="Konfigurace první startovací rychlost", zorder=2
# )
#
# plt.errorbar(
#     E_m2, E_carka_m2, xerr=E_chyba_m2, yerr=E_carka_chyba_m2,
#     fmt="s", color="red", ecolor="lightcoral", elinewidth=1,
#     capsize=2, markersize=5, label="Konfigurace druhá startovací rychlost", zorder=2
# )

def ideal_pripad(x, a, b):
    return a * x + b

popt, pcov = curve_fit(ideal_pripad, p_rych, p_int)
std_errs = np.sqrt(np.diag(pcov))

a, b = popt
chyba_a, chyba_b = std_errs

print(f"{TextColor.BOLD}=== Výsledky lineárního fitu ==={TextColor.END}")
print(
    f"{TextColor.BOLD}{TextColor.UNDERLINE}Sklon a = {round_val_err(a, chyba_a, True)}{TextColor.END}\n " +
    f"╚═({a} ± {chyba_a})\n")
print(
    f"{TextColor.BOLD}{TextColor.UNDERLINE}Posun b = {round_val_err(b, chyba_b, True)}{TextColor.END}\n " +
    f"╚═({b} ± {chyba_b})\n")
print("====================================\n")

max_val = np.max(np.concatenate((p_int, p_rych)))
x_vals = np.linspace(0, max_val * 1.1, 1000)

plt.plot(
    p_rych,
    a * p_rych + b,
    color="red",
    label=r"Fit: $\Delta p_{\text{int}} = a\cdot x + b$",
)



plt.xlabel(r"$\Delta p_{rych}$ [$\mathrm{g \cdot m \cdot s^{-1}}$]", fontsize=11)
plt.ylabel(r"$\Delta p_{int}$ [$\mathrm{g \cdot m \cdot s^{-1}}$]", fontsize=11)

# plt.gca().xaxis.set_major_formatter(comma_formatter)
# plt.gca().yaxis.set_major_formatter(comma_formatter)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "zavislost_pint_na_prych.svg"
plt.savefig(svg_name, format="svg")
plt.close()
