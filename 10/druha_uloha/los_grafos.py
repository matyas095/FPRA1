import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy.optimize import curve_fit

# Načtení dat
X_Vals_1_time = np.load("data/group_1_data.npy", allow_pickle=True)
Y_Vals_1_position = np.load("data/group_2_data.npy", allow_pickle=True)
x_err = 0.001015
y_err = 0.01155

X_Vals_1_time = X_Vals_1_time[:, 1].astype(float)
Y_Vals_1_position = Y_Vals_1_position[:, 1].astype(float)


# Definice fitovací funkce (tlumené kmity)
def damped_oscillation(t, phi_max, delta, omega, phi_0):
  return phi_max * np.exp(-delta * t) * np.sin(omega * t + phi_0)


# Počáteční odhady parametrů [phi_max, delta, omega, phi_0]
phi_max_guess = np.max(np.abs(Y_Vals_1_position))
delta_guess = 0.1
omega_guess = 2.0 * np.pi
phi_0_guess = 0.0
p0 = [phi_max_guess, delta_guess, omega_guess, phi_0_guess]

# Provedení fitu pomocí curve_fit
popt, pcov = curve_fit(
    damped_oscillation, X_Vals_1_time, Y_Vals_1_position, p0=p0
)
perr = np.sqrt(np.diag(pcov))  # Směrodatné odchylky parametrů

# Rozbalení parametrů
phi_max_opt, delta_opt, omega_opt, phi_0_opt = popt

# Výpočet vlastní frekvence omega_0 podle vztahu omega_0 = sqrt(omega^2 + delta^2)[cite: 7, 10]
omega_0 = np.sqrt(omega_opt**2 + delta_opt**2)
grad_omega0 = np.array([delta_opt / omega_0, omega_opt / omega_0])

pcov_sub = pcov[1:3, 1:3]

var_omega0 = grad_omega0.T @ pcov_sub @ grad_omega0
err_omega0 = np.sqrt(var_omega0)

# Výpis výsledků do konzole
print("--- Výsledky fitu ---")
print(f"Maximální amplituda (phi_max) = {phi_max_opt:.4f} ± {perr[0]:.4f}")
print(f"Koeficient útlumu (delta)     = {delta_opt:.4f} ± {perr[1]:.4f}")
print(f"Úhlová frekvence (omega)      = {omega_opt:.4f} ± {perr[2]:.4f}")
print(f"Fázový posun (phi_0)          = {phi_0_opt:.4f} ± {perr[3]:.4f}")
print("-" * 40)
print(f"Vlastní frekvence (omega_0)   = {omega_0:.4f} ± {err_omega0:.4f} rad/s")

t_smooth = np.linspace(X_Vals_1_time.min(), X_Vals_1_time.max(), 1000)
y_fit = damped_oscillation(t_smooth, *popt)

plt.figure(figsize=(9, 5))

# Vykreslení naměřených bodů
plt.errorbar(
    X_Vals_1_time,
    Y_Vals_1_position,
    xerr=x_err,
    yerr=y_err,
    fmt="o",  # Styl bodů (kolečka)
    color="b",  # Barva bodů
    ecolor="gray",  # Barva chybových úseček
    elinewidth=1,  # Tloušťka čáry chybové úsečky
    capsize=2,  # Velikost „stříšek“ na koncích úseček
    markersize=5,
    label="Naměřená data s chybami",
    zorder=1,
)

# Vykreslení proložené křivky fitu
plt.plot(
    t_smooth,
    y_fit,
    color="r",
    linestyle="-",
    linewidth=2,
    label=(
        "Fit: $\\varphi_{\\max} e^{-\\delta t} \\sin(\\omega t + \\varphi_0)$"
    ),
    zorder=2,
)

plt.xlabel("$t$ [s]", fontsize=11)
plt.ylabel("$\\varphi$ [rad]", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = "outputs/02-angular_position_plot.svg"
plt.savefig(svg_name, format="svg")