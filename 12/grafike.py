import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import FuncFormatter

from pathlib import Path
import sys

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"

# SETTING EXTR(AS) FUNCS
current_dir = Path(__file__).resolve().parent

root_dir = current_dir
while not (root_dir / "extr").exists() and root_dir != root_dir.parent:
    root_dir = root_dir.parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# ACTUAL SCRIPTS
from extr.funcs.rounder import round_val_err
from extr.data.colors import TextColor

Q = np.array([
    [
        14, 17, 22, 29, 43  # a = 4
    ],
    [
        7, 11, 17, 30, 42  # a = 5
    ],
    [
        8, 11, 18, 33, 30  # a = 6
    ],
    [
        5, 14, 28, 31, 42  # a = 7
    ],
    [
        1, 7, 19, 20, 24  # a = 8
    ]
]) # µC
Q_na_druhou = Q ** 2

F_mat = np.array([
    [
        0.6, 1.5, 1.7, 2.3, 2.9  # a = 4
    ],
    [
        0.20, 0.60, 1.15, 1.90, 2.00  # a = 5
    ],
    [
        0.10, 0.30, 0.65, 1.30, 1.50  # a = 6
    ],
    [
        0.08, 0.30, 0.52, 0.97, 1.23  # a = 7
    ],
    [
        0.03, 0.26, 0.39, 0.80, 0.90  # a = 8
    ]
]) * 10 ** 3 # mN -> µN

A_as = []

for i, (Q, F) in enumerate(zip(Q_na_druhou, F_mat)):
    a = 4 + i
    print(f"{TextColor.BOLD}{TextColor.UNDERLINE}{TextColor.GREEN}Pro vzdálenost a = {a} cm:{TextColor.END}")

    (A_a, b), pcov1 = np.polyfit(Q, F, 1, cov=True)
    A_a_err, b_err = np.sqrt(np.diag(pcov1))
    A_as.append([A_a, A_a_err])

    print(f"{TextColor.BOLD}=== Výsledky fitu ==={TextColor.END}")
    print(
        f"{TextColor.BOLD}{TextColor.UNDERLINE}Sklon A_a = {round_val_err(A_a, A_a_err, True)}{TextColor.END}\n" +
        f"╚═({A_a} ± {A_a_err})\n")
    print(
        f"{TextColor.BOLD}{TextColor.UNDERLINE}Parametr b = {round_val_err(b, b_err, True)}{TextColor.END}\n" +
        f"╚═({b} ± {b_err})")
    print("=====================\n")


    def idealni_model(x, A_a):
        return A_a * x


    (A_a_ideal), pcov = curve_fit(idealni_model, Q, F)

    std_err_A = np.sqrt(np.diag(pcov))[0]

    print(f"{TextColor.BOLD}=== Výsledky ideálního (b = 0) ==={TextColor.END}")
    print(
        f"{TextColor.BOLD}{TextColor.UNDERLINE}Ideální Sklon A_a = {round_val_err(A_a_ideal[0], std_err_A, True)}{TextColor.END}\n " +
        f"╚═({A_a_ideal[0]} ± {std_err_A})\n")
    print("====================================\n")

    plt.figure(figsize=(9, 5))

    random_color = np.random.rand(3)
    chyba_Q = 0.004 ** 2
    chyba_F = 0.00006 * 10 ** 6 # µN

    plt.plot(
        Q,
        A_a * Q + b,
        color="red",
        label=fr"Fit: $F = A_{a}\cdot Q^2 + b$",
    )

    plt.errorbar(
        Q,
        F,
        xerr=chyba_Q,
        yerr=chyba_F,
        fmt="o",
        color=random_color,
        ecolor="gray",
        elinewidth=1,
        capsize=2,
        markersize=5,
        label=f"Vypočtená data s chybami",
        zorder=1,
    )

    plt.xlabel("$Q^2$ [µC]", fontsize=11)
    plt.ylabel(r"$F$ [µN]", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()

    svg_name = output_dir / "A_a" / f"{a}.svg"
    plt.savefig(svg_name, format="svg")
    plt.close()

A_as = np.array(A_as)
a_vzd = np.array([
    4, 5, 6, 7, 8
]) * 1e-2 # m
a_vys = 1 / (a_vzd ** 2)

def model_prochazejici_pocatkem(x, S):
    return S * x


poptS, pcovS = curve_fit(model_prochazejici_pocatkem, a_vys, A_as[:, 0])
std_err_S = np.sqrt(np.diag(pcovS))[0]

S = poptS[0]
print("\n\n\n")
print(f"{TextColor.BOLD}=== Výsledky sklonu S ==={TextColor.END}")
print(
    f"{TextColor.BOLD}{TextColor.UNDERLINE}Sklon S = {round_val_err(S, std_err_S, True)}{TextColor.END}\n " +
    f"╚═({S} ± {std_err_S})\n")
print("====================================\n")

plt.figure(figsize=(9, 5))

random_color = np.random.rand(3)
chyba_a_vys = 0.2

a_vys_prodlouzene = np.linspace(-0.05, max(a_vys) * 1.1, 1000)

plt.plot(
    a_vys_prodlouzene,
    S * a_vys_prodlouzene,
    color="red",
    label=fr"Fit: $A_a = S \cdot 1/a^2$",
)

plt.errorbar(
    a_vys,
    A_as[:, 0],
    xerr=chyba_a_vys,
    yerr=A_as[:, 1],
    fmt="o",
    color="black",
    ecolor="gray",
    elinewidth=1,
    capsize=2,
    markersize=5,
    label=f"Vypočtená data s chybami",
    zorder=1,
)

plt.xlabel(r"$1/a^2$ [$\mathrm{m^{-2}}$]", fontsize=11)
plt.ylabel(r"$A_a$ [$\mathrm{N/C^2}$]", fontsize=11)

comma_formatter = FuncFormatter(lambda x, pos: f"{x:.2f}".replace(".", ","))
plt.gca().xaxis.set_major_formatter(comma_formatter)
plt.gca().yaxis.set_major_formatter(comma_formatter)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "inv_As" / f"inverzos.svg"
plt.savefig(svg_name, format="svg")
plt.close()

epsilon_0 = 1 / (16 * np.pi * S)

chyba_epsilon_0_vypocet = 1 / (16 * np.pi * S ** 2) * std_err_S

print(f"{TextColor.BOLD}=== Výsledky permitivity epsilon_0 ==={TextColor.END}")
print(
    f"{TextColor.BOLD}{TextColor.UNDERLINE}Permitivita epsilon_0 = {round_val_err(epsilon_0, chyba_epsilon_0_vypocet, True)}*10^{-12} F/m{TextColor.END}\n " +
    f"╚═({epsilon_0} ± {chyba_epsilon_0_vypocet})\n")
print("====================================\n")
