import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

t = np.array(
    [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450],
    dtype=float,
)
count_rate = np.array(
    [421, 374, 337, 296, 267, 238, 211, 190, 170, 151, 138, 125, 111, 102, 91, 86],
    dtype=float,
)


# R(t) = R0 * exp(-lambda * t)
def decay_model(time, r0, decay_lambda):
  return r0 * np.exp(-decay_lambda * time)


popt, pcov = curve_fit(decay_model, t, count_rate, p0=[count_rate[0], 0.0035])
r0_fit, lambda_fit = popt
r0_err, lambda_err = np.sqrt(np.diag(pcov))

t_half = np.log(2) / lambda_fit
t_half_err = (np.log(2) / (lambda_fit**2)) * lambda_err

slope, intercept = np.polyfit(t, np.log(count_rate), 1)
lambda_lin = -slope
t_half_lin = np.log(2) / lambda_lin

print(f"Nelineární fit: R0 = {r0_fit:.2f} ± {r0_err:.2f}")
print(f"Nelineární fit: lambda = {lambda_fit:.6f} ± {lambda_err:.6f} s^-1")
print(f"Nelineární fit: T_1/2 = {t_half:.2f} ± {t_half_err:.2f} s")
print(f"Lineární fit ln(R): T_1/2 = {t_half_lin:.2f} s")

t_smooth = np.linspace(t.min(), t.max(), 300)

plt.figure(figsize=(8, 5))
plt.scatter(t, count_rate, color="tab:blue", label="Naměřená data (count rate)")
plt.plot(
    t_smooth,
    decay_model(t_smooth, r0_fit, lambda_fit),
    color="tab:red",
    linewidth=2,
    label=rf"Exponenciální fit: $T_{{1/2}} = {t_half:.1f} \pm {t_half_err:.1f}\text{{ s}}$",
)

plt.xlabel("$t$ [s]")
plt.ylabel("$n$ [-]")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()

svg_name = "zavislost_na_case_idk_adrianus.png"
plt.savefig(svg_name, format="png")
plt.close()