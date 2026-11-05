import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

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
])
Q_na_druhou = Q ** 2

F_mat = np.array([
    [
        0.0006, 0.0015, 0.0017, 0.0023, 0.0029  # a = 4
    ],
    [
        0.0002, 0.0006, 0.00115, 0.0019, 0.002  # a = 5
    ],
    [
        0.0001, 0.0003, 0.00065, 0.0013, 0.0015  # a = 6
    ],
    [
        0.00008, 0.0003, 0.00052, 0.00097, 0.00123  # a = 7
    ],
    [
        0.00003, 0.00026, 0.00039, 0.0008, 0.0009  # a = 8
    ]
]) * 10 ** 3

for i, (Q, F) in enumerate(zip(Q_na_druhou, F_mat)):
    a = 4 + i
    print(f"{TextColor.BOLD}{TextColor.UNDERLINE}{TextColor.GREEN}Pro vzdálenost a = {a} cm:{TextColor.END}")

    (A_a, b), pcov1 = np.polyfit(Q, F, 1, cov=True)
    A_a_err, b_err = np.sqrt(np.diag(pcov1))

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
    chyba_Q = 0.004
    chyba_F = 0.00012 * 10 ** 3

    plt.plot(
        Q,
        A_a * Q + b,
        color="red",
        label=fr"Fit: $F = A_a\cdot Q^2 + b$",
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
