import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sympy
from scipy.optimize import curve_fit



# --- 1. VSTUPNÍ PARAMETRY A KONSTANTY ---
delta = 0.9631
D_mm = 14.2  # průměr koulí jiskřiště [mm]
D_cm = D_mm / 10.0

# Deskový kondenzátor
r_desky_cm = 8.4983  # poloměr desek kondenzátoru [cm]
r_desky_m = r_desky_cm / 100.0
S_desky = np.pi * (r_desky_m**2)  # plocha desek [m^2]
d_mm = 7.2  # vzdálenost desek kondenzátoru [mm]
d_m = d_mm / 1000.0
epsilon_0 = 8.854187817e-12  # permitivita vakua [F/m]

# --- 2. NAMĚŘENÁ DATA ---
s_mm = np.array([1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 1.50, 2.50])
F_arr = np.array(
    [0.3090, 0.3384, 0.4316, 0.4464, 0.4562, 0.4611, 0.4758, 0.4807, 0.3286, 0.3483]
)

# --- 3. VÝPOČET NAPĚTÍ U A f(s/D) ---
U_kV = d_m * np.sqrt((2 * F_arr) / (epsilon_0 * S_desky)) / 1000.0

s_cm = s_mm / 10.0
s_D = s_mm / D_mm
zavorka = 1.0 + 0.757 / np.sqrt(delta * D_cm)
f_sD = (27.75 * zavorka * delta * s_cm) / U_kV

# --- 4. CHYBY / UNCERTAINTIES ---
sigma_sD = 0.007  # Zadaná chyba pro s/D
sigma_f = (27.75 * zavorka * delta * (sigma_sD * D_cm)) / U_kV  # Chyba pro f(s/D)

# Seřazení podle s/D
idx = np.argsort(s_D)
s_D_sorted = s_D[idx]
f_sD_sorted = f_sD[idx]
sigma_f_sorted = sigma_f[idx]

# --- VÝPIS HODNOT A CHYB DO KONZOLE ---
print("--- VÝPIS NAMĚŘENÝCH A SPOČTENÝCH HODNOT ---")
print(f"{'s/D':<12} | {'f(s/D)':<22}")
print("-" * 38)
for sd, f_val, f_err in zip(s_D_sorted, f_sD_sorted, sigma_f_sorted):
  sd_str = f"{sd:.2f}".replace(".", ",")
  f_str = f"{f_val:.2f}".replace(".", ",")
  err_str = f"{f_err:.2f}".replace(".", ",")
  print(f"{sd_str:<12} | {f_str} ± {err_str}")
print("-" * 38 + "\n")


# --- 5. FITOVÁNÍ KŘIVKY S VÁHAMI A CHYBAMI ---
def lin_func_constrained(x, k):
  return k * x + 1.0


popt, pcov = curve_fit(
    lin_func_constrained,
    s_D_sorted,
    f_sD_sorted,
    sigma=sigma_f_sorted,
    absolute_sigma=True,
)
k_fit = popt[0]
k_err = np.sqrt(pcov[0, 0])

# Explicitní naformátování parametrů pro fit
k_fit_str = f"{k_fit:.2f}".replace(".", ",")
k_err_str = f"{k_err:.2f}".replace(".", ",")

print(f"Fit s f(0)=1: f(s/D) = ({k_fit_str} ± {k_err_str}) * (s/D) + 1\n")

# --- 6. VYKRESLENÍ GRAFU S CHYBOVÝMI ÚSEČKAMI ---
s_D_fine = np.linspace(0, np.max(s_D_sorted) * 1.05, 200)

plt.figure(figsize=(8, 5))

# Vykreslení bodů s chybovými úsečkami
plt.errorbar(
    s_D_sorted,
    f_sD_sorted,
    xerr=sigma_sD,
    yerr=sigma_f_sorted,
    fmt="ro",
    ecolor="black",
    elinewidth=1.2,
    capsize=3,
    label="Naměřená data",
    zorder=5,
)

plt.plot(
    s_D_fine,
    lin_func_constrained(s_D_fine, k_fit),
    "b-",
    label=(
        f"Fit: $({k_fit_str} \\pm {k_err_str}) \\cdot"
        r" \left(\frac{s}{D}\right) + 1$"
    ),
    linewidth=2,
)

# --- FORMÁTOVÁNÍ OS ---
xaxis_formatter = ticker.FuncFormatter(
    lambda x, pos: f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")
)
yaxis_formatter = ticker.FuncFormatter(
    lambda x, pos: f"{x:.2f}".replace(".", ",")
)

plt.gca().xaxis.set_major_formatter(xaxis_formatter)
plt.gca().yaxis.set_major_formatter(yaxis_formatter)

plt.xlabel(r"$\frac{s}{D}$ [-]")
plt.ylabel(r"$f\left(\frac{s}{D}\right)$ [-]")
plt.xlim(left=0)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()

# Uložení grafu do SVG
svg_name = "fit_funkce_f_sD_with_errors.svg"
plt.savefig(svg_name, format="svg")
plt.show()