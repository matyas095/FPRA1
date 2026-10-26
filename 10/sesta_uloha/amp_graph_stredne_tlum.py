import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs" / "stredni_tlum"

# 1. Výsledky fitu z kalibrační přímky (Úkol 5)
a = 0.4645
u_a = 0.0100
b = -0.1951
u_b = 0.0723

# Vlastní frekvence z Úkolu 2[cite: 1]
omega_0_fixed = 3.916
I_slabe = 0.05  # <--- ZMĚŇTE NA SVOU HODNOTU PROUDU (např. 0.2 pro 200 mA, nebo podle zápisů)

# 2. Naměřená data pro slabě tlumené kyvadlo (Úkol 6)[cite: 1, 8]
U_data = np.array([
    7.58, 7.43, 7.53, 7.73, 7.86, 7.89, 8.05, 7.90, 7.31, 7.6
])
A_data_slabe = np.array([
    6.0995, 6.0995, 6.1055, 6.0835, 6.1135, 6.1005, 6.1145, 6.1025, 6.081, 6.068
])  # Zde si doplňte své amplitudy

A_err = 0.00817

# 3. Výpočet úhlových frekvencí Omega a jejich chyb
u_U = 0.005 * U_data + 0.08
Omega_data = a * U_data + b
Omega_err = np.sqrt((U_data * u_a) ** 2 + u_b**2 + (a * u_U) ** 2)

# 4. Výpočet delta pro slabě tlumené kyvadlo pomocí vztahu (5)
# Zde zadejte proud I [v ampérech], který jste nastavili na zdroji pro slabě tlumené kyvadlo:

a, u_a = 0.010, 0.003
b, u_b = 2.89, 0.12
c, u_c = 0.71, 0.04

delta_slabe_fixed = a * np.exp(b * I_slabe) + c
d_da = np.exp(b * I_slabe)
d_db = a * I_slabe * np.exp(b * I_slabe)
d_dc = 1.0
d_dI = a * b * np.exp(b * I_slabe)

u_I = 0.0009

u_delta = np.sqrt(
    (d_da * u_a) ** 2 + (d_db * u_b) ** 2 + (d_dc * u_c) ** 2 + (d_dI * u_I) ** 2
)
print(f"Spočtené delta pro slabé tlumení: {delta_slabe_fixed:.4f} ± {u_delta:.4f} s^-1")


# 5. Teoretický model rezonanční křivky (vztah 19)[cite: 4, 5]
def resonance_slabe(Omega, B):
    return B / np.sqrt(
        (omega_0_fixed**2 - Omega**2) ** 2 + 4 * (delta_slabe_fixed**2) * (Omega**2)
    )

# Provedení fitu (fítujeme konstantu B)
popt, pcov = curve_fit(
    resonance_slabe,
    Omega_data,
    A_data_slabe,
    p0=[100.0],
    sigma=np.full_like(A_data_slabe, A_err),
    absolute_sigma=True,
)
B_fit = popt[0]
B_err = np.sqrt(pcov[0, 0])

print(f'Nalezená konstanta B = {B_fit:.4f} ± {B_err:.4f}')

# 6. Vykreslení grafu
Omega_fine = np.linspace(1, 7, 500)
A_fit = resonance_slabe(Omega_fine, B_fit)

plt.figure(figsize=(8, 5))
plt.errorbar(
    Omega_data,
    A_data_slabe,
    xerr=Omega_err,
    yerr=A_err,
    fmt='bo',
    ecolor='gray',
    elinewidth=1,
    capsize=3,
    label='Naměřená data',
    zorder=5,
)

plt.plot(
    Omega_fine,
    A_fit,
    color='brown',
    linestyle='--',
    label='Fit funkce $\\frac{B}{\\sqrt{(\\omega_0^2 - \\Omega^2)^2 + 4\\delta^2\\Omega^2}}$',
)
plt.xlabel(r'$\Omega$ [rad/s]')
plt.ylabel('$A$ [-]')
plt.xlim(1, 7)
plt.legend()
plt.grid(True)

svg_name = output_dir / f"outtering.svg"
plt.savefig(svg_name, format="svg")

plt.close()