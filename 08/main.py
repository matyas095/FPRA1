import sympy as sy
import numpy as np

eps, U, d, S = sy.symbols('eps U d S')

F = 1 / 2 * eps * (U ** 2)/(d ** 2) * S

dF_deps = F.diff(eps)
dF_dU = F.diff(U)
dF_dd = F.diff(d)
dF_dS = F.diff(S)

print(sy.latex(dF_deps))
print(sy.latex(dF_dU))
print(sy.latex(dF_dd))
print(sy.latex(dF_dS))