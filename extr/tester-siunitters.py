from siunitters import Length
import numpy as np

m1 = Length(3, "m", ERROR=20)
m2 = Length(5, "cm", ERROR=0.23)

print(m1 + m2)

print(np.sqrt(20 ** 2 + (0.23 / 100) ** 2))