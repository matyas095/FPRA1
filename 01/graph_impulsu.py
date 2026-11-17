from typing import Tuple
import shutil

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.optimize import curve_fit
from pathlib import Path
from scipy.integrate import simpson
import sys

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

terminal_size = shutil.get_terminal_size()

def setConsoleDimensions():
    try:
      terminal_size = shutil.get_terminal_size()
      console_width = terminal_size.columns
      console_height = terminal_size.lines
    except (OSError, ValueError):
      console_width = 80
      console_height = 24

    return console_width, console_height

console_width, console_height = setConsoleDimensions()

# ACTUAL SCRIPTS
from extr.funcs.rounder import round_val_err
from extr.data.colors import TextColor


def calculate_momentum_with_error(m, v, v_prime, dm, dv, dv_prime) -> Tuple[float, float]:
    """Vypočítá hybnost i s chybou

    :param m: Hmotnost vozíku
    :param v: Rychlost před srážkou
    :param v_prime: Rychlost po srážce
    :param dm: Chyba hmotnosti
    :param dv: Chyba rychlosti před srážkou
    :param dv_prime: Chyba rychlosti po srážce
    """
    p = m * (v_prime - v)

    # 2. Partial derivatives
    dp_dm = v_prime - v
    dp_dv_prime = m
    dp_dv = -m

    sigma_p = np.sqrt(
        (dp_dm * dm) ** 2
        + (dp_dv_prime * dv_prime) ** 2
        + (dp_dv * dv) ** 2
    )

    return abs(p), sigma_p

# Vstupní data
t1 = np.array([
    [
        6.956, 6.957, 6.958, 6.959, 6.96, 6.961, 6.962, 6.963, 6.964, 6.965, 6.966, 6.967, 6.968, 6.969
    ],
    [
        1.802, 1.803, 1.804, 1.805, 1.806, 1.807, 1.808, 1.809, 1.81, 1.811, 1.812, 1.813, 1.814
    ],
    [
        0.876, 0.877, 0.878, 0.879, 0.88, 0.881, 0.882, 0.883, 0.884, 0.885, 0.886, 0.887
    ],
    [
        1.549, 1.55, 1.551, 1.552, 1.553, 1.554, 1.555, 1.556, 1.557, 1.558, 1.559, 1.56
    ],
    [
        1.385, 1.386, 1.387, 1.388, 1.389, 1.39, 1.391, 1.392, 1.393, 1.394, 1.395, 1.396
    ],
    [
        4.209, 4.21, 4.211, 4.212, 4.213, 4.214, 4.215, 4.216, 4.217, 4.218, 4.219, 4.22
    ],
    [
        1.419, 1.42, 1.421, 1.422, 1.423, 1.424, 1.425, 1.426, 1.427, 1.428, 1.429
    ],
    [
        2.463, 2.464, 2.465, 2.466, 2.467, 2.468, 2.469, 2.47, 2.471, 2.472, 2.473
    ],
    [
        0.876, 0.877, 0.878, 0.879, 0.88, 0.881, 0.882, 0.883, 0.884, 0.885, 0.886, 0.887
    ],
    [
        0.381, 0.382, 0.383, 0.384, 0.385, 0.386, 0.387, 0.388, 0.389, 0.39, 0.391, 0.392
    ]
], dtype=object)
t_chyba = 0.001 # s
F1 = np.array([
    [
        0, 0, 2.7, 7.6, 11.7, 13.3, 12.8, 11.4, 8.2, 4.4, 1.5, -0.2, 0.3, -0.1
    ],
    [
        0, 0.3, 5.1, 9.4, 12.8, 13.5, 12.5, 10.2, 6.9, 3.2, 0.6, 0.1, -0.1
    ],
    [
        0, 1.5, 6, 9.8, 12, 11.9, 10.8, 8.3, 5.1, 2.1, 0.1, 0.1
    ],
    [
        0, 0.5, 3.8, 7, 9.1, 9.9, 9, 7.3, 4.8, 2.5, 0.9, -0.2
    ],
    [
        0, 0.4, 3.6, 7, 9.3, 10.2, 9.4, 7.6, 5.1, 2.7, 1, -0.2
    ],
    [
        0, 0.4, 3.5, 6.3, 8.7, 9.5, 9, 7.2, 5, 2.6, 0.8, -0.1
    ],
    [
        0, 3.3, 7.3, 11, 12.4, 11.7, 10.1, 7.4, 4, 1.3, -0.2
    ],
    [
        0, 2.5, 6.9, 10.5, 12.1, 11.7, 10.2, 7.1, 3.9, 1.3, -0.2
    ],
    [
        0, 0.1, 3, 6.4, 9, 9.9, 9.4, 7.8, 5.3, 3, 1.2, -0.1
    ],
    [
        0, 0.4, 3.2, 6.1, 8.2, 8.9, 8.5, 6.9, 4.6, 2.4, 0.7, -0.2
    ]
], dtype=object) # N
F_chyba = 0.03 # N

t2 = np.array([
    [
        3.21, 3.211, 3.212, 3.213, 3.214, 3.215, 3.216, 3.217, 3.218, 3.219, 3.22, 3.221, 3.222, 3.223, 3.224, 3.225, 3.226, 3.227, 3.228, 3.229, 3.23, 3.231, 3.232, 3.233, 3.234, 3.235, 3.236, 3.237, 3.238, 3.239, 3.24, 3.241, 3.242, 3.243, 3.244, 3.245, 3.246, 3.247, 3.248, 3.249, 3.25, 3.251, 3.252, 3.253, 3.254, 3.255, 3.256, 3.257, 3.258, 3.259, 3.26, 3.261, 3.262, 3.263, 3.264, 3.265, 3.266, 3.267, 3.268, 3.269, 3.27, 3.271, 3.272, 3.273, 3.274, 3.275, 3.276, 3.277, 3.278, 3.279, 3.28, 3.281, 3.282, 3.283, 3.284, 3.285, 3.286, 3.287, 3.288, 3.289, 3.29, 3.291, 3.292, 3.293, 3.294, 3.295, 3.296, 3.297, 3.298, 3.299, 3.3, 3.301, 3.302, 3.303, 3.304, 3.305, 3.306, 3.307, 3.308, 3.309, 3.31, 3.311, 3.312, 3.313, 3.314, 3.315, 3.316, 3.317, 3.318, 3.319, 3.32, 3.321, 3.322, 3.323, 3.324, 3.325, 3.326, 3.327, 3.328, 3.329, 3.33, 3.331, 3.332, 3.333, 3.334, 3.335, 3.336
    ],
    [
        2.692, 2.693, 2.694, 2.695, 2.696, 2.697, 2.698, 2.699, 2.7, 2.701, 2.702
    ],
    [
        0.838, 0.839, 0.84, 0.841, 0.842, 0.843, 0.844, 0.845, 0.846, 0.847, 0.848, 0.849
    ],
    [
        3.021, 3.022, 3.023, 3.024, 3.025, 3.026, 3.027, 3.028, 3.029, 3.03, 3.031, 3.032, 3.033
    ],
    [
        2.61, 2.611, 2.612, 2.613, 2.614, 2.615, 2.616, 2.617, 2.618, 2.619, 2.62, 2.621, 2.622, 2.623
    ],
    [
        3.712, 3.713, 3.714, 3.715, 3.716, 3.717, 3.718, 3.719, 3.72, 3.721, 3.722, 3.723, 3.724, 3.725, 3.726
    ],
    [
        1.919, 1.92, 1.921, 1.922, 1.923, 1.924, 1.925, 1.926, 1.927, 1.928, 1.929, 1.93, 1.931, 1.932, 1.933, 1.934, 1.935, 1.936, 1.937, 1.938, 1.939, 1.94, 1.941, 1.942, 1.943, 2.593, 2.594, 2.595, 2.596, 2.597, 2.598, 2.599, 2.6
    ],
    [
        1.587, 1.588, 1.589, 1.59, 1.591, 1.592, 1.593, 1.594, 1.595, 1.596, 1.597, 1.598, 1.599
    ],
    [
        2.857, 2.858, 2.859, 2.86, 2.861, 2.862, 2.863, 2.864, 2.865, 2.866, 2.867
    ],
    [
        2.415, 2.416, 2.417, 2.418, 2.419, 2.42, 2.421, 2.422, 2.423, 2.424, 2.425, 2.426, 2.427
    ]
], dtype=object)

F2 = np.array([
    [
        0, 0, 0, 0, 0, 0, 0, 0, 0.1, 9.3, 20.6, 26.3, 27.5, 24.7, 17.7, 10.6, 4.5, -0.8, 0.3, 0.1, -0.1, 0.2, -0.2, 0.1, 0.1, -0.2, 0.2, -0.1, 0, 0, -0.1, 0.1, 0, -0.1, 0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0, 0, 0.1, 0, 0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [
        -0.1, 1.9, 14.4, 21.7, 26.1, 26.7, 22.3, 14.8, 8.7, 2.9, -0.5
    ],
    [
        0, 5.7, 17.1, 23.7, 26.8, 25.4, 19.3, 12.8, 6.4, 0.9, 0.2, -0.1
    ],
    [
        0, 0.6, 11.6, 20.8, 25.4, 26.3, 23.1, 16.1, 8.9, 3.4, -0.6, 0.4, 0
    ],
    [
        0, 0, 0.2, 9.9, 19.6, 24.9, 26.1, 23.5, 16.8, 9.5, 4.1, -0.6, 0.4, -0.1
    ],
    [
        0, 5.1, 16.6, 23.2, 26.2, 25.6, 20.3, 12.9, 6.6, 1.1, 0.2, 0.1, -0.1, 0.1, 0
    ],
    [
        0, 0, 0, 0, 0, 0, 1, 13.7, 22.6, 26.7, 27, 23.2, 15.7, 8.4, 2.9, -0.4, 0.3, 0.1, 0.1, 0.1, -0.1, 0.1, 0, -0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [
        0, 0.1, 9.7, 19, 25, 26.7, 24.4, 17.8, 10.2, 5.2, -0.2, 0.3, -0.1
    ],
    [
        0, 2.3, 13.4, 21.1, 25.1, 25.2, 20.3, 14.1, 7.6, 2.3, -0.2
    ],
    [
        0, 1.2, 11, 20.8, 26.2, 27, 22.7, 15.7, 9.1, 3.7, -0.7, 0.4, 0
    ]
], dtype=object)



t3 = np.array([
    [
        1.215, 1.216, 1.217, 1.218, 1.219, 1.22, 1.221, 1.222, 1.223, 1.224
    ],
    [
        2.003, 2.004, 2.005, 2.006, 2.007, 2.008, 2.009, 2.01, 2.011, 2.012, 2.013
    ],
    [
        0.421, 0.422, 0.423, 0.424, 0.425, 0.426, 0.427, 0.428, 0.429, 0.43, 0.431
    ],
    [
        2.278, 2.279, 2.28, 2.281, 2.282, 2.283, 2.284, 2.285, 2.286, 2.287, 2.288
    ],
    [
        1.055, 1.056, 1.057, 1.058, 1.059, 1.06, 1.061, 1.062, 1.063, 1.064, 1.065
    ],
    [
        1.088, 1.089, 1.09, 1.091, 1.092, 1.093, 1.094, 1.095, 1.096, 1.097, 1.098, 1.099, 1.1
    ],
    [
        0.182, 0.183, 0.184, 0.185, 0.186, 0.187, 0.188, 0.189, 0.19, 0.191, 0.192
    ],
    [
        1.132, 1.133, 1.134, 1.135, 1.136, 1.137, 1.138, 1.139, 1.14, 1.141, 1.142
    ],
    [
        0.614, 0.615, 0.616, 0.617, 0.618, 0.619, 0.62, 0.621, 0.622, 0.623, 0.624, 0.625, 0.626
    ],
    [
        0.053, 0.054, 0.055, 0.056, 0.057, 0.058, 0.059, 0.06, 0.061, 0.062, 0.063, 0.064
    ]
], dtype=object)
F3 = np.array([
    [
        0, 13.5, 29.1, 38.2, 39.8, 34.8, 25.1, 14.5, 5.3, -0.8
    ],
    [
        0, 0, 10, 26.5, 36.1, 39.6, 35.9, 26.7, 16, 6.8, -0.6
    ],
    [
        0, 7.6, 23.4, 34, 39.5, 36.9, 28, 17.4, 9, 0.9, 0.3
    ],
    [
        0, 2.2, 15.1, 25, 30.7, 30.8, 26.3, 18.6, 10.9, 4, -0.6
    ],
    [
        0, 9.2, 24.8, 33.9, 37.2, 34.4, 26, 16.2, 7.3, 0.7, 0.1
    ],
    [
        0, 0.8, 14.4, 26.3, 32.7, 34.4, 30, 21.8, 12.9, 5.2, 0.3, 0.4, -0.2
    ],
    [
        0, 4.5, 20.8, 31.1, 36.6, 35, 27.4, 19, 9.7, 2.6, -0.5
    ],
    [
        0, 10.4, 24.9, 33.3, 36, 32.6, 24.3, 15.2, 6.3, 1.3, 0
    ],
    [
        0, 3, 17, 28.9, 35.7, 35.4, 29.6, 21.6, 11.9, 4.6, -0.8, 0.8, -0.1
    ],
    [
        0, 4.8, 22.1, 33, 38.9, 37.6, 30.4, 20.6, 10.3, 3.1, -0.8, 0.8
    ]
], dtype=object)

t_s = [t1, t2, t3]
F_s = [F1, F2, F3]


comma_formatter = FuncFormatter(lambda x, pos: f"{x:.1f}".replace(".", ","))

# ========================
#  t F Graf
# ========================
totalAreas = []

for j, (t_arr, F_arr) in enumerate(zip(t_s, F_s)):
    print(f"Kontrola t{j + 1}: {len(t_arr)}")
    print(f"Kontrola F{j + 1}: {len(F_arr)}")
    totalAreas.append([])

    subfigures = []

    for i, (t, F) in enumerate(zip(t_arr, F_arr)):
        t = np.array(t)
        F = np.array(F)
        plt.figure(figsize=(9, 5))
        plt.errorbar(
            t, F, xerr=t_chyba, yerr=F_chyba,
            fmt="o", color="blue", ecolor="lightblue", elinewidth=1,
            capsize=2, markersize=5, label="Naměřené hodnoty s chybami", zorder=2
        )

        # area = np.trapezoid(F, t)
        area_simpson_mN = simpson(F * 1000, x=t)
        integral_coarse_mN = simpson(F[::2] * 1000, t[::2])
        area_simpson = simpson(F, x=t)
        integral_coarse = simpson(F[::2], t[::2])

        error_estimate = abs(area_simpson - integral_coarse) / 15
        error_estimate_coarse_mN = abs(area_simpson_mN - integral_coarse_mN) / 15
        totalAreas[j].append((area_simpson, error_estimate))

        label_fill = f"S = {round_val_err(area_simpson_mN, error_estimate_coarse_mN, True)} [$\\mathrm{{mN \\cdot s}}$]"
        plt.fill_between(t, F, color="skyblue", alpha=0.4, label=label_fill)

        plt.xlabel(r"$t$ [$\mathrm{s}$]", fontsize=11)
        plt.ylabel(r"$F$ [$\mathrm{N}$]", fontsize=11)

        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(fontsize=10)
        plt.tight_layout()

        svg_name = output_dir / f"F{j + 1}" / f"{i + 1}.svg"
        svg_name.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(svg_name, format="svg")
        plt.close()

        label_letter = chr(ord("a") + i)

        subfigures_content = rf"""\begin{{subfigure}}[t]{{0.3\textwidth}}
            \centering
            \includesvg[width=\textwidth]{{img/graphs/6/F{j + 1}/{i + 1}}}
            \caption{{
                Plocha {label_fill.replace("[", "").replace("]", "")}
            }}
            \label{{fig:integrales-{j + 1}{label_letter}}}
        \end{{subfigure}}"""

        if (i + 1) % 3 == 0 and i < len(t_arr) - 1:
            subfigures_content += "\n\n    \\vspace{0.5em}\n"
        elif i < len(t_arr) - 1:
            subfigures_content += "%\n    \\hfill\n"

        subfigures.append(subfigures_content)

    totalAreas_vals = np.array([item[0] for item in totalAreas[j]]) * 1000

    suma_S = sum(totalAreas_vals) / len(totalAreas_vals)
    std_S = np.std(totalAreas_vals, ddof=1) / np.sqrt(len(totalAreas_vals))

    if j + 1 == 1:
        addon = "Pro první stupeň odrazu pístku"
    elif j + 1 == 2:
        addon = "Pro druhý stupeň odrazu pístku"
    else:
        addon = "Pro třetí stupeň odrazu pístku"

    latex_content = rf"""\begin{{figure}}[H]
        \centering

        {"".join(subfigures)}

        \caption{{
            Naměřené hodnoty síly $F$ v závislosti na čase $t$. Výpočet plochy pod integrálem, kde celková plocha vychází $S={round_val_err(suma_S, std_S, True).replace("±", r"\pm")}\,\mathrm{{mN\cdot s^{{-1}}}}$, vypočtené jako aritmetický průměr a její směrodatná odchylka. {addon}. Vypočteno skrze program Python \cite{{GitHubMAT}}.
        }}
        \label{{fig:integrales-{j + 1}}}
    \end{{figure}}
    """

    file_name = output_dir / "tex_inputs" / f"F{j + 1}.tex"
    file_name.parent.mkdir(parents=True, exist_ok=True)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(latex_content)


# ========================
#  Hybnosti
# ========================
m = 203.94000 # g
sigma_m = 1.61182 # g

v_s = np.array([
    [
        0.30740,
        0.00802
    ],
    [
        0.56730,
        0.00802
    ],
    [
        0.76330,
        0.01545
    ]
]) # val, err
v_prime_s = np.array([
    [
        0.04060,
        0.00236
    ],
    [
        0.06302,
        0.00530
    ],
    [
        0.07597,
        0.01321
    ]
]) # val, err

for i, (sublist, v_arr, v_prime_arr) in enumerate(zip(totalAreas, v_s, v_prime_s)):
    print("=" * console_width)
    v, v_err = v_arr
    v_prime, v_prime_err = v_prime_arr

    data = np.array(sublist) * 1000
    vals = data[:, 0]
    errs = data[:, 1]

    delta_p_int = np.sum(vals) / len(vals)
    delta_p_int_err = np.std(vals, ddof=1) / np.sqrt(len(vals))
    delta_delta_p_int = delta_p_int_err / delta_p_int * 100
    print("Δp_int :", i + 1, round_val_err(delta_p_int, delta_p_int_err, True), f"δ = {delta_delta_p_int}")

    delta_p_rych, delta_p_rych_err = calculate_momentum_with_error(
        m, v, v_prime, sigma_m, v_err, v_prime_err
    )
    delta_delta_p_rych = delta_p_rych_err / abs(delta_delta_p_int)
    sigma_delta_p_rych = abs(delta_p_int - delta_p_rych) / delta_p_rych_err
    print("Δp_rych :", round_val_err(delta_p_rych, delta_p_rych_err, True),
          f"δ = {delta_delta_p_rych} %", f"σ = {sigma_delta_p_rych}")

    # for j, (val, err) in enumerate(sublist):
    #     print(i + 1, j + 1, val, err)
