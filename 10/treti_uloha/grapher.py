import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

from scipy.optimize import curve_fit

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"
subfolders = sorted(
    [f for f in data_dir.iterdir() if f.is_dir()], key=lambda f: f.name
)

def damped_oscillation(t, phi_max, delta, omega, phi_0, offset):
  return phi_max * np.exp(-delta * t) * np.sin(omega * t + phi_0) + offset

x_err = 0.001015
y_err = 0.01155

delta_storages = []

for index, path in enumerate(subfolders, start=1):
    groupName = path.name

    firstGroup = np.load(rf"{path}/group_1_data.npy", allow_pickle=True)
    secondGroup = np.load(rf"{path}/group_2_data.npy", allow_pickle=True)

    x_vals = firstGroup[:, 1].astype(float)
    y_vals = secondGroup[:, 1].astype(float)

    phi_max_guess = np.max(np.abs(y_vals))
    delta_guess = 0.1
    omega_guess = 2.0 * np.pi
    phi_0_guess = 0.0
    offset_guess = np.mean(y_vals[-10:])
    p0 = [phi_max_guess, delta_guess, omega_guess, phi_0_guess, offset_guess]

    popt, pcov = curve_fit(
      damped_oscillation, x_vals, y_vals, p0=p0
    )
    perr = np.sqrt(np.diag(pcov))

    phi_max_opt, delta_opt, omega_opt, phi_0_opt, offset_opt = popt

    t_smooth = np.linspace(x_vals.min(), x_vals.max() + 0.1, 1000)
    y_fit = damped_oscillation(t_smooth, *popt)

    print(f"--- Výsledky fitu {groupName} ---")
    print(f"Maximální amplituda (phi_max) = {phi_max_opt:.4f} ± {perr[0]:.4f}")
    print(f"Koeficient útlumu (delta)     = {delta_opt:.4f} ± {perr[1]:.4f}")
    print(f"Úhlová frekvence (omega)      = {omega_opt:.4f} ± {perr[2]:.4f}")
    print(f"Fázový posun (phi_0)          = {phi_0_opt:.4f} ± {perr[3]:.4f}")
    print(f"Offset                        = {offset_opt:.4f} ± {perr[4]:.4f}")
    print("-" * 40)

    delta_storages.append((groupName,
        delta_opt, perr[1]
    ))

    plt.figure(figsize=(9, 5))

    random_color = np.random.rand(3)

    # Vykreslení dat
    plt.errorbar(
      x_vals,
      y_vals,
      xerr=x_err,
      yerr=y_err,
      fmt="o",
      color=random_color,
      ecolor="gray",
      elinewidth=1,
      capsize=2,
      markersize=5,
      label=f"Naměřená data s chybami",
      zorder=1,
    )

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
    plt.ylabel(f"$\\varphi_{index}$ [rad]", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()

    svg_name = output_dir / f"03-angular_position_{groupName}.svg"
    plt.savefig(svg_name, format="svg")

    plt.close()

I_vals = np.array([
    1.2, 1.4, 1.6, 1.8, 2.0
])
I_errs = np.array([
    0.14, 0.14, 0.15, 0.15, 0.16
])

plt.figure(figsize=(9, 5))

def exp_func(I, a, b, c):
    return a * np.exp(b * I) + c

groupName, delta_vals, delta_err = zip(*delta_storages)

popt, pcov = curve_fit(exp_func, I_vals, delta_vals, sigma=delta_err, absolute_sigma=True)
perr = np.sqrt(np.diag(pcov))
a_opt, b_opt, c_opt = popt
print(f"Parametry fitu: a = {a_opt:.4f} ± {perr[0]:.4f}, b = {b_opt:.4f} ± {perr[1]:.4f}, c = {c_opt:.4f} ± {perr[2]:.4f}")

omega_0 = 3.916
I_krit = np.log((omega_0 - c_opt) / a_opt) / b_opt
da = -1.0 / (a_opt * b_opt)
db = -I_krit / b_opt
dc = -1.0 / (b_opt * (omega_0 - c_opt))

J = np.array([da, db, dc])

I_krit_err = np.sqrt(np.dot(J, np.dot(pcov, J)))

# 3. Výsledek
print(f"Vypočtený kritický proud: I_krit = {I_krit:.4f} ± {I_krit_err:.4f} A")

I_smooth = np.linspace(min(I_vals) - 0.03, max(I_vals) + 0.13, 200)
delta_fit = exp_func(I_smooth, *popt)

plt.errorbar(
  I_vals,
  delta_vals,
  xerr=I_errs,
  yerr=delta_err,
  fmt="o",
  color="b",
  ecolor="gray",
  elinewidth=1,
  capsize=2,
  markersize=5,
  label=fr"Vypočtené hodnot $\delta$ v závislosti na $I$",
  zorder=1,
)

plt.plot(
  I_smooth,
  delta_fit,
  color="r",
  linestyle="-",
  linewidth=2,
  label=(
      "Fit: $\\varphi_{\\max} e^{-\\delta t} \\sin(\\omega t + \\varphi_0)$"
  ),
  zorder=2,
)

plt.xlabel("$I$ [A]", fontsize=11)
plt.ylabel(r"$\delta$ [$s^{-1}$]", fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()

svg_name = output_dir / f"03-delta_fit.svg"
plt.savefig(svg_name, format="svg")

plt.close()