import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs" / "bez_tlum"

# 1. Výsledky fitu z kalibrační přímky (Úkol 5)
a = 0.4645
u_a = 0.0100
b = -0.1951
u_b = 0.0723

omega_0_fixed = 3.916  # Vlastní frekvence z Úkolu 2 [rad/s]
delta_fixed = 0.154    # Koeficient útlumu z Úkolu 3 [s^-1]

# 2. Naměřená data z Úkolu 6 (napětí a amplitudy)
U_data = np.array([
    7.9, 7.92, 8.01, 8.08, 8.11, 7.84, 7.6, 7.56, 7.42, 7.35
])
A_data = np.array([
    6.017, 5.695, 6.0135, 6.0555, 6.238, 6.0595, 6.073, 6.052, 6.053, 6.0715
])

# Vypočtená chyba amplitudy
A_err = 0.00817

# 3. Výpočet úhlových frekvencí Omega a jejich chyb u_Omega pro každé napětí U
u_U = 0.005 * U_data + 0.08
Omega_data = a * U_data + b
Omega_err = np.sqrt((U_data * u_a) ** 2 + u_b**2 + (a * u_U) ** 2)

# 5. Teoretický model rezonanční křivky (vztah 19)[cite: 4, 5]
def resonance_fixed(Omega, B):
    return B / np.sqrt(
        (omega_0_fixed**2 - Omega**2) ** 2 + 4 * (delta_fixed**2) * (Omega**2)
    )

# Provedení fitu (fítujeme pouze konstantu B)
popt, pcov = curve_fit(
    resonance_fixed,
    Omega_data,
    A_data,
    p0=[100.0],
    sigma=np.full_like(A_data, A_err),
    absolute_sigma=True,
)
B_fit = popt[0]
B_err = np.sqrt(pcov[0, 0])

# Výpis výsledků
print(f'Nalezená konstanta B = {B_fit:.4f} ± {B_err:.4f}')

# 6. Vykreslení výsledného grafu s chybovými úsečkami na obou osách
Omega_fine = np.linspace(1, 7, 500)
A_fit = resonance_fixed(Omega_fine, B_fit)

plt.figure(figsize=(8, 5))
plt.errorbar(
    Omega_data,
    A_data,
    xerr=Omega_err,
    yerr=A_err,
    fmt='ro',
    ecolor='gray',
    elinewidth=1,
    capsize=3,
    label='Naměřená data s chybami',
    zorder=5,
)

plt.plot(
    Omega_fine,
    A_fit,
    color='blue',
    linestyle='--',
    label='Fit funkce $\\frac{B}{\\sqrt{(\\omega_0^2 - \\Omega^2)^2 + 4\\delta^2\\Omega^2}}$',
)
plt.xlabel(r'$\Omega$ [rad/s]')
plt.ylabel('$A$ [-]')
plt.xlim(1, 7)
plt.legend()
plt.grid(True)

svg_name = output_dir / f"outter.svg"
plt.savefig(svg_name, format="svg")

plt.close()