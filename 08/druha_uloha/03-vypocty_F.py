import numpy as np
import sympy as sp
import pandas as pd

# Zadané hodnoty hmotnosti v gramech
hodnoty_m = np.array([
    31.5, 34.5, 44, 45.5, 46.5, 47, 48.5, 49, 33.5, 35.5
])

# Převod na kg pro výpočet síly v N
g_val = 9.81
hodnoty_m_kg = hodnoty_m / 1000.0
hodnoty_F = hodnoty_m_kg * g_val
print("Hodnoty F (v N):", hodnoty_F)

# --- (SymPy) ---
m, g = sp.symbols("m g")

# Zdroje chyb (převod chyby m na kilogramy)
chyba_F_m_kg = 10.000_05 / 1000.0  # [kg]
chyba_F_g = 0.0                   # [nemáme chybu g]

# Definice funkce F (s převodem m na kg uvnitř, aby seděly jednotky)
F = (m / 1000.0) * g

# Parciální derivace pomocí SymPy
dF_dm = F.diff(m)
dF_dg = F.diff(g)

print("Parciála dF_dm: ", dF_dm)
print("Parciála dF_dg: ", dF_dg)

# Převedení SymPy výrazů na standardní pythonovské funkce pomocí lambdify
# Pozor: dF_dm závisí na g, dF_dg závisí na m (nebo jsou to konstanty)
f_dF_dm = sp.lambdify(g, dF_dm, 'numpy')
f_dF_dg = sp.lambdify(m, dF_dg, 'numpy')

# Výpočet hodnot derivací
derivace_m = f_dF_dm(g_val)
derivace_g = f_dF_dg(hodnoty_m_kg)

# Vlastní výpočet chyby nepřímé
chyby_F = np.sqrt(
    (derivace_m * chyba_F_m_kg)**2 +
    (derivace_g * chyba_F_g)**2
)

print("\nChyby F pro jednotlivé hodnoty (v N):")
for i, (m_val, f_val, err_val) in enumerate(zip(hodnoty_m, hodnoty_F, chyby_F)):
    print(f"Měření {i+1}: m = {m_val} g -> F = {f_val:.4f} N ± {err_val:.4f} N")

np.save('soubory/hodnoty_F.npy', hodnoty_F)

rounder = 4
format_str = f"{{:.{rounder}f}}"
vysledky_text = [
    f"{format_str.format(u).replace('.', ',')} ± {format_str.format(err).replace('.', ',')}"
    for u, err in zip(hodnoty_F, chyby_F)
]

df = pd.DataFrame({
    r'$F \, [\mathrm{N}]$': vysledky_text
})

# Zkopírování rovnou do schránky pro Excel
df.to_clipboard(excel=True, index=False)