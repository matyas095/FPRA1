import numpy as np
import sympy as sp

omega0, a, b, c = sp.symbols("omega0 a b c")

I_krit = sp.ln((omega0 - c)/a) / b

dI_domega0 = I_krit.diff(omega0)
dI_a = I_krit.diff(a)
dI_b = I_krit.diff(b)
dI_c = I_krit.diff(c)

sigma_err = sp.sqrt(
    (dI_domega0 * omega0) ** 2 +
    (dI_a * a) ** 2 +
    (dI_b * b) ** 2 +
    (dI_c * c) ** 2
)

print(sp.latex(sigma_err))