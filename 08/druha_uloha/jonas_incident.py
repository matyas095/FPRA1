import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. Data z tabulky
x_data = np.array([0.14, 0.28, 0.42, 0.56, 0.69, 0.83, 0.97, 1.11, 0.21, 0.35])
y_data = np.array([2.97, 3.41, 3.55, 3.69, 3.83, 3.97, 4.11, 4.25, 2.08, 2.34])

# 2. Definice funkce s fixním počátkem f(0) = 1
def linear_fixed(x, a):
    return a * x + 1.0

# 3. Fitování směrnice 'a'
popt, pcov = curve_fit(linear_fixed, x_data, y_data)
a = popt[0]
a_err = np.sqrt(pcov[0][0])

print(f"Směrnice a = {a:.2f} ± {a_err:.2f}")

# 4. Vykreslení
plt.figure(figsize=(8, 5))
plt.scatter(x_data, y_data, marker='x', color='blue', label='naměřená data')

x_fit = np.linspace(0, 1.35, 100)
y_fit = linear_fixed(x_fit, a)

plt.plot(x_fit, y_fit, 'k--', label=f'Fit: f(x) = ({a:.2f} ± {a_err:.2f})x + 1')

plt.xlabel(r'$s/D$ [-]')
plt.ylabel(r'$f(s/D)$ [-]')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower right')
plt.xlim(0, 1.4)
plt.ylim(0.8, 5.2)

plt.show()