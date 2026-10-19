import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# --- 1. VSTUPNÍ PARAMETRY A KONSTANTY ---
delta = 0.9631
D_mm = 14.2  # průměr koulí jiskřiště [mm]
D_cm = D_mm / 10.0

# Deskový kondenzátor
r_desky_cm = 8.4983  # poloměr desek kondenzátoru [cm][cite: 16]
r_desky_m = r_desky_cm / 100.0
S_desky = np.pi * (r_desky_m ** 2)  # plocha desek [m^2]
d_mm = 7.2  # vzdálenost desek kondenzátoru [mm][cite: 3]
d_m = d_mm / 1000.0
epsilon_0 = 8.854187817e-12  # permitivita vakua [F/m]

# --- 2. NAMĚŘENÁ DATA ---
s_mm = np.array([1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 1.50, 2.50])
F_arr = np.array([0.3090, 0.3384, 0.4316, 0.4464, 0.4562, 0.4611, 0.4758, 0.4807, 0.3286, 0.3483])

# --- 3. VÝPOČET NAPĚTÍ U A f(s/D) ---
# U ze vztahu (13): U = d * sqrt(2*F / (epsilon_0 * S)) v kilovoltech[cite: 3]
U_kV = d_m * np.sqrt((2 * F_arr) / (epsilon_0 * S_desky)) / 1000.0

# Výpočet bezrozměrného poměru s/D a hodnot f(s/D)
s_cm = s_mm / 10.0
s_D = s_mm / D_mm
zavorka = 1.0 + 0.757 / np.sqrt(delta * D_cm)
f_sD = (27.75 * zavorka * delta * s_cm) / U_kV

# Seřazení podle s/D pro plynulou čáru v grafu
idx = np.argsort(s_D)
s_D_sorted = s_D[idx]
f_sD_sorted = f_sD[idx]

# --- 4. FITOVÁNÍ KŘIVKY (Lineární fit) ---
def lin_func(x, k, q):
    return k * x + q

popt, _ = curve_fit(lin_func, s_D_sorted, f_sD_sorted)
k_fit, q_fit = popt

print(f"Nalezený předpis fitu: f(s/D) = {k_fit:.4f} * (s/D) + {q_fit:.4f}")

# --- 5. VYKRESLENÍ A ULOŽENÍ DO SVG ---
s_D_fine = np.linspace(np.min(s_D_sorted), np.max(s_D_sorted), 200)

plt.figure(figsize=(8, 5))
plt.plot(s_D_sorted, f_sD_sorted, 'ro', label='Naměřené body', markersize=7, zorder=5)
plt.plot(
    s_D_fine,
    lin_func(s_D_fine, *popt),
    'b-',
    label=f'Fit: ${k_fit:.3f}x + {q_fit:.3f}$',
    linewidth=2,
)

plt.title('Závislost korekční funkce $f(s/D)$ na poměru $s/D$')
plt.xlabel('Poměr $s/D$ [-]')
plt.ylabel('Korekční funkce $f(s/D)$ [-]')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Uložení grafu ve formátu SVG
svg_name = 'fit_funkce_f_sD_final.svg'
plt.savefig(svg_name, format='svg')
plt.show()

print(f"Graf byl úspěšně uložen jako '{svg_name}'.")