from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

script_dir = Path(__file__).parent
output_dir = script_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

U_vals = np.array([6.4, 6.973333333, 7.26, 7.59, 7.986666667])
U_errs = np.array([0.053, 0.057, 0.057, 0.059, 0.062])

# Původní otáčky v RPM
otacky_rpm = np.array([26.5, 29.1, 30.3, 31.9, 33.5])
otacky_rpm_errs = np.array([0.11325, 0.11455, 0.11515, 0.11595, 0.11675])

# PŘEPOČET Z RPM NA ÚHLOVOU FREKVENCI Ω [rad/s]: vzorec (RPM / 60) * 2 * pi
Omega_vals = otacky_rpm * (2 * np.pi / 60)
Omega_errs = otacky_rpm_errs * (2 * np.pi / 60)


def calibration_func(U, a, b):
  return a * U + b


# Fitujeme závislost úhlové frekvence Omega na napětí U
popt, pcov = curve_fit(
    calibration_func,
    U_vals,
    Omega_vals,
    sigma=Omega_errs,
    absolute_sigma=True,
)
perr = np.sqrt(np.diag(pcov))
a_opt, b_opt = popt

print(f"--- Výsledky kalibračního fitu (v rad/s) ---")
print(f"Sklon (a) = {a_opt:.4f} ± {perr[0]:.4f}")
print(f"Korekce (b) = {b_opt:.4f} ± {perr[1]:.4f}")
print("-" * 40)

U_smooth = np.linspace(min(U_vals) - 0.2, max(U_vals) + 0.2, 200)
Omega_fit = calibration_func(U_smooth, *popt)

plt.figure(figsize=(9, 5))
random_color = np.random.rand(3)

plt.errorbar(
    U_vals,
    Omega_vals,
    xerr=U_errs,
    yerr=Omega_errs,
    fmt="o",
    color=random_color,
    ecolor="gray",
    elinewidth=1,
    capsize=2,
    markersize=5,
    label="Naměřená data s chybami",
    zorder=1,
)

plt.plot(
    U_smooth,
    Omega_fit,
    color="r",
    linestyle="-",
    linewidth=2,
    label=fr"Kalibrační přímka: $\Omega = a\cdot U + b$",
    zorder=2,
)

plt.xlabel("$U$ [V]", fontsize=11)
plt.ylabel(r"$\Omega$ [rad/s]", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / "05-kalibracni_krivka.svg"
plt.savefig(svg_name, format="svg")
plt.close()