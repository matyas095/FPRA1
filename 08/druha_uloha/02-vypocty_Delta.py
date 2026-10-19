import numpy as np
import sympy as sp
import pandas as pd

# ---------------------------------------------------------
# 1. SYMPY Definice
# ---------------------------------------------------------

# Definice symbolických proměnných
b, t = sp.symbols('b t')

# Vzorec pro napětí U
delta = b / 760 * (273 + 20) / (273 + t)
print("Vypsání funkce:")
print(sp.latex(delta))

# Parciální derivace funkce Delta
dDelta_db = delta.diff(b)
dDelta_dt = delta.diff(t)
print("Vypsání parciálních derivací:")
print(sp.latex(dDelta_db))
print(sp.latex(dDelta_dt))

# Převedení symbolických výrazů na NumPy funkce
f_delta = sp.lambdify((b, t), delta, 'numpy')
f_dDelta_db = sp.lambdify((b, t), dDelta_db, 'numpy')
f_dDelta_dt = sp.lambdify((b, t), dDelta_dt, 'numpy')

# ---------------------------------------------------------
# 2. Číselné hodnoty
# ---------------------------------------------------------
# Delta Funkce
b_Vals = 741.7
delta_b = 1.2
t_Vals = 23.9
delta_t = 0.2

# Hodnota delta
delta_Val = f_delta(b_Vals, t_Vals)

# Hodnoty derivací
der_b = f_dDelta_db(b_Vals, t_Vals)
der_t = f_dDelta_dt(b_Vals, t_Vals)

delta_err_val = np.sqrt(
    (der_b * delta_b)**2 +
    (der_t * delta_t)**2
)

# ---------------------------------------------------------
# 3. výstup
# ---------------------------------------------------------
print("Výstup delty:")
print(f"{delta_Val:.4f} ± {delta_err_val:.4f}")

# Ukládání
np.savez("soubory/vypocty_delta.npz", delta_val=delta_Val, delta_err_val=delta_err_val)

# Načtení zpět (funguje jako slovník)
soubor = np.load("soubory/vypocty_delta.npz")
delta_val = soubor["delta_val"]
delta_err_val = soubor["delta_err_val"]