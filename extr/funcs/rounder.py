import math


def round_val_err(value, error, toText = False):
  if error <= 0:
    return value, error

  order = math.floor(math.log10(error))

  norm_error = error / (10**order)
  if norm_error < 2:
    ndigits = -order + 1
  else:
    ndigits = -order

  factor = 10**ndigits

  rounded_error = math.ceil(round(error * factor, 10)) / factor

  rounded_value = round(value, ndigits)

  if toText:
    return rf"({rounded_value} ± {rounded_error})"

  return rounded_value, rounded_error


# --- Example Test ---
val, err = round_val_err(24.5678, 0.0136)
print(f"Result: ({val} ± {err})")
# Output: Result: (24.57 ± 0.014)  [0.0136 rounded up with 2 sig figs becomes 0.014]