import numpy as np
import sympy as sp
import pandas as pd

# ---------------------------------------------------------
# 1. SYMPY Definice
# ---------------------------------------------------------

# Definice symbolických proměnných
U, d = sp.symbols('U d')

# Vzorec pro napětí U
E_p = U / d

# Parciální derivace funkce E_p
dU_dU = E_p.diff(U)
dU_dd = E_p.diff(d)
print("Vypsání parciálních derivací:")
print(sp.latex(dU_dU))
print(sp.latex(dU_dd))

# Převedení symbolických výrazů na NumPy funkce
f_E_p = sp.lambdify((U, d), E_p, 'numpy')
f_dU_dU = sp.lambdify((U, d), dU_dU, 'numpy')
f_dU_dd = sp.lambdify((U, d), dU_dd, 'numpy')


# ---------------------------------------------------------
# 2. ČÍSELNÉ HODNOTY A VÝPOČET CHYBY (NumPy)
# ---------------------------------------------------------
U_val = np.load('hodnoty/hodnoty_U.npy') # Hodnoty U
delta_U = np.load('chyby/delta_U.npy') # Chyby U
d_val = np.array([
    15, 14, 13, 12, 11, 10, 9, 8, 7, 6
]) / 1000 # mm -> m

# Absolutní chyby jednotlivých veličin (ve základních SI jednotkách)
delta_d = 0.5 / 1000.0    # Chyba vzdálenosti mm -> m

# Výpočet hodnoty U
E_p_vals = f_E_p(U_val, d_val)

# Výpočet parciálních derivací v daném bodě
der_U = f_dU_dU(U_val, d_val)
der_d = f_dU_dd(U_val, d_val)

# Výpočet chyby napětí Delta U metodou RSS (Root Sum Square)
delta_E_p = np.sqrt(
    (der_U * delta_U)**2 +
    (der_d * delta_d)**2
)

# ---------------------------------------------------------
# 3. VÝSTUP
# ---------------------------------------------------------
rounder = 2
E_p_vals = E_p_vals / 1000
delta_E_p = delta_E_p / 1000

print("\nVypočetný E_p:")
for i, (e_p_val, err_val) in enumerate(zip(E_p_vals, delta_E_p)):
    print(f"{i+1}: {e_p_val:.{rounder}f} ± {err_val:.{rounder}f} kV/m")

E_p_zaokrouhlene = np.round(E_p_vals, rounder)
delta_zaokrouhlene = np.round(delta_E_p, rounder)

formát_str = f"{{:.{rounder}f}}"
vysledky_text = [
    f"{formát_str.format(u).replace('.', ',')} ± {formát_str.format(err).replace('.', ',')}"
    for u, err in zip(E_p_vals, delta_E_p)
]

df = pd.DataFrame({
    r'$E_p \, [\mathrm{kV\cdot m^{-1}}]$': vysledky_text
})

# Zkopírování rovnou do schránky pro Excel
df.to_clipboard(excel=True, index=False)