import numpy as np
import matplotlib.pyplot as plt

Q_V = np.array([1.52, 1.84, 3.38, 2.98, 2.63, 2.66, 2.72, 2.63, 1.95, 1.34, 2.17])
p2 = 99860.0
p1 = np.array([100408, 100213, 100193, 100271, 100320, 100418, 100281, 100320, 100330, 100144, 100428])

y = (p1**2 - p2**2) / (2 * p2)
Q_V_SI = Q_V * 1e-6

p, cov = np.polyfit(Q_V_SI, y, 1, cov=True)
a = p[0]
b = p[1]

errors = np.sqrt(np.diag(cov))
a_err = errors[0]
b_err = errors[1]

print(f"Směrnice a = {a:.4e} ± {a_err:.4e} [Pa*s/m^3]")

a_plot, b_plot = np.polyfit(Q_V, y, 1)

plt.figure(figsize=(8, 5))
plt.plot(Q_V, y, 'ob', label='Naměřená data')

x_fit = np.linspace(min(Q_V) - 0.2, max(Q_V) + 0.2, 100)
plt.plot(x_fit, a_plot * x_fit + b_plot, 'r--', label=f'Lineární fit: $y = {a_plot:.2f}x {b_plot:+.2f}$')

plt.xlabel(r'$V_t$ [ml/s]', fontsize=12)
plt.ylabel(r'$\frac{p_1^2 - p_2^2}{2p_2}$ [Pa]', fontsize=12)
plt.title(r'Závislost $\frac{p_1^2 - p_2^2}{2p_2} = f(V_t)$', fontsize=14)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11)

plt.tight_layout()
plt.savefig('zavislost.svg', format='svg', bbox_inches='tight')