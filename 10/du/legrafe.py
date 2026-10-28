from matplotlib import pyplot as plt
import numpy as np

t = np.linspace(
    0, 4, 500
)
phi_0 = 1.0
Omega_0 = 3.0
delta = 2.0

phi_poloha = phi_0 * np.exp(-delta * t) * (1 + delta * t)

phi_rychlost = Omega_0 * t * np.exp(-delta * t)

plt.figure(figsize=(9, 5))

plt.plot(t, phi_poloha, label=r"$\varphi(t) = \varphi_0 e^{-\delta t}(1+\delta t)$", color="blue", lw=2)
plt.xlabel("$t$ [s]")
plt.ylabel(r"$\varphi$ [rad]")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = "du-polohovost.svg"
plt.savefig(svg_name, format="svg")
plt.close()

plt.plot(t, phi_rychlost, label=r"$\varphi(t) = \Omega_0 t e^{-\delta t}$", color="red", lw=2)
plt.xlabel("$t$ [s]")
plt.ylabel(r"$\varphi$ [rad]")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = "du-rychlost.svg"
plt.savefig(svg_name, format="svg")