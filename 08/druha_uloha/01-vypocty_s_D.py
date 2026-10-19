import numpy as np
import pandas as pd

s = np.array([
    1, 2, 3, 4, 5, 6, 7, 8, 1.5, 2.5
]) / 10 # mm
D = np.array([
    14.2, 14.3, 14.2
]) / 10 # průměr (mm)
bar_D = np.sum(D) / 3;
delta_D = np.std(D)

s_D = s / bar_D
print(s_D)
delta_s_D = np.sqrt(
    (1 / bar_D * 0.01) ** 2 +
    (-s / (bar_D ** 2) * 0.005) ** 2
)

for i, (s_D_val, err_val) in enumerate(zip(s_D, delta_s_D)):
    print(f"{i + 1}: {s_D_val:.5f} ± {err_val:.5f}");

np.savez("soubory/vypocty_s-D.npz", s_D=s_D, delta_s_D=delta_s_D)

rounder = 4
format_str = f"{{:.{rounder}f}}"
vysledky_text = [
    f"{format_str.format(u).replace('.', ',')} ± {format_str.format(err).replace('.', ',')}"
    for u, err in zip(s_D, delta_s_D)
]

df = pd.DataFrame({
    r'$s_D \, [-]$': vysledky_text
})

# Zkopírování rovnou do schránky pro Excel
df.to_clipboard(excel=True, index=False)