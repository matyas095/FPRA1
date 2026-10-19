import numpy as np
import sympy as sp
import pandas as pd

# ---------------------------------------------------------
# 1. SYMPY Definice
# ---------------------------------------------------------

# Definice symbolických proměnných
d, F, eps0, S = sp.symbols('d F eps0 S')

# Vzorec pro napětí U
U_expr = d * sp.sqrt((2 * F) / (eps0 * S))

# Parciální derivace funkce U podle jednotlivých proměnných
dU_dd = U_expr.diff(d)
dU_dF = U_expr.diff(F)
dU_dS = U_expr.diff(S)

# Převedení symbolických výrazů na NumPy funkce
f_U = sp.lambdify((d, F, S, eps0), U_expr, 'numpy')
f_dU_dd = sp.lambdify((d, F, S, eps0), dU_dd, 'numpy')
f_dU_dF = sp.lambdify((d, F, S, eps0), dU_dF, 'numpy')
f_dU_dS = sp.lambdify((d, F, S, eps0), dU_dS, 'numpy')


# ---------------------------------------------------------
# 2. ČÍSELNÉ HODNOTY A VÝPOČET CHYBY (NumPy)
# ---------------------------------------------------------

# Permitivita vakua (konstanta bez chyby)
eps0_val = 8.8541878128e-12  # [F/m]

# Vstupní naměřené hodnoty (ve základních SI jednotkách: m, N, m^2)
d_val = np.array([
    15, 14, 13, 12, 11, 10, 9, 8, 7, 6
])
F_val = np.load('hodnoty_F.npy')              # Síla v Newtonech
S_val = 0.022689            # Plocha desek v m^2

# Absolutní chyby jednotlivých veličin (ve základních SI jednotkách)
delta_d = 0.001 / 1000.0    # Chyba vzdálenosti (např. 0.001 mm = 1 µm)
delta_F = 0.0001            # Chyba síly v Newtonech
delta_S = 0.0000908         # Chyba plochy v m^2

# Výpočet hodnoty U
U_val = f_U(d_val, F_val, S_val, eps0_val)

# Výpočet parciálních derivací v daném bodě
der_d = f_dU_dd(d_val, F_val, S_val, eps0_val)
der_F = f_dU_dF(d_val, F_val, S_val, eps0_val)
der_S = f_dU_dS(d_val, F_val, S_val, eps0_val)

# Výpočet chyby napětí Delta U metodou RSS (Root Sum Square)
delta_U = np.sqrt(
    (der_d * delta_d)**2 +
    (der_F * delta_F)**2 +
    (der_S * delta_S)**2
)

# ---------------------------------------------------------
# 3. VÝSTUP
# ---------------------------------------------------------
print("\nVypočetný napětí:")
for i, (u_val, err_val) in enumerate(zip(U_val, delta_U)):
    print(f"{i+1}: {u_val:.2f} ± {err_val:.2f} U")



U_zaokrouhlene = np.round(U_val, 0)
delta_zaokrouhlene = np.round(delta_U, 0)

vysledky_text = [f"{u:.2f} ± {err:.2f}" for u, err in zip(U_zaokrouhlene, delta_zaokrouhlene)]

df = pd.DataFrame({
    r'$U \, [\mathrm{V}]$': vysledky_text
})

# Zkopírování rovnou do schránky pro Excel
df.to_clipboard(excel=True, index=False)