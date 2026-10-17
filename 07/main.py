import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

r = 0.39e-3       # [m] poloměr kapiláry
r_err = 0.01e-3   # [m] nejistota poloměru

l = 91.6e-3       # [m] délka kapiláry
l_err = 0.1e-3    # [m] nejistota délky

V_t_mls = np.array([1.52, 1.84, 3.38, 2.98, 2.63, 2.66, 2.72, 2.63, 1.95, 1.34, 2.17])
V_t_err_mls = np.full_like(V_t_mls, 0.05)  # [ml/s]

V_t = V_t_mls * 1e-6
V_t_err = V_t_err_mls * 1e-6

p2 = 99860.0  # [Pa]
delta_p_hPa = np.array([5.5, 3.5, 3.3, 4.1, 4.6, 5.6, 4.2, 4.6, 4.7, 2.8, 5.7])
p1 = p2 + delta_p_hPa * 100.0  # [Pa]

y_data = (p1**2 - p2**2) / (2.0 * p2)  # [Pa]
y_err = np.full_like(y_data, 70.0)    # [Pa]

def linear_func(x, alpha, b):
    return alpha * x + b

popt, pcov = curve_fit(linear_func, V_t, y_data, sigma=y_err, absolute_sigma=True)

alpha = popt[0]
b = popt[1]

alpha_err = np.sqrt(pcov[0, 0])
b_err = np.sqrt(pcov[1, 1])

eta = (alpha * np.pi * (r**4)) / (8.0 * l)

rel_alpha_err = alpha_err / abs(alpha)
rel_r_err = r_err / r
rel_l_err = l_err / l

rel_eta_err = np.sqrt(rel_alpha_err**2 + (4 * rel_r_err)**2 + rel_l_err**2)
eta_err = abs(eta) * rel_eta_err

print("=== VÝSLEDKY ===")
print(f"Směrnice alpha: {alpha:.4e} ± {alpha_err:.4e} Pa*s/m^3")
print(f"Posun b:        {b:.2f} ± {b_err:.2f} Pa")
print(f"Viskozita eta:  ({eta:.2e} ± {eta_err:.2e}) Pa*s (kg*m^-1*s^-1)")

plt.figure(figsize=(9, 6), dpi=150)

plt.errorbar(V_t_mls, y_data,
             xerr=V_t_err_mls,
             yerr=y_err,
             fmt='o',
             color='blue',
             ecolor='lightblue',
             elinewidth=1.5,
             capsize=3,
             label='Naměřená data s chybou',
             zorder=3)

# Lineární fit
x_fit_mls = np.linspace(min(V_t_mls) * 0.85, max(V_t_mls) * 1.15, 100)
x_fit_m3s = x_fit_mls * 1e-6
y_fit = linear_func(x_fit_m3s, alpha, b)

label_fit = f'Lineární fit: $y = ({alpha:.2e} \\pm {alpha_err:.2e})x + ({b:.1f} \\pm {b_err:.1f})$'
plt.plot(x_fit_mls, y_fit, color='red', linestyle='--', label=label_fit, zorder=2)

plt.title(r'Závislost $\frac{p_1^2 - p_2^2}{2p_2} = f(V_t)$ s chybovými úsečkami', fontsize=13)
plt.xlabel(r'$V_t$ [ml/s]', fontsize=12)
plt.ylabel(r'$\frac{p_1^2 - p_2^2}{2p_2}$ [Pa]', fontsize=12)

plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()

plt.savefig('zavislost-oprava.svg', format='svg')
plt.show()