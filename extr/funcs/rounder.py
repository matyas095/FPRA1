import math


def round_val_err(value, error, toText=False):
    value = float(value)
    error = float(error)

    if error <= 0:
        ndigits = 1
        rounded_error = round(error, ndigits)
        rounded_value = round(value, ndigits)
    else:
        order = math.floor(math.log10(error))

        norm_error = error / (10 ** order)
        if norm_error < 2:
            ndigits = -order + 1
        else:
            ndigits = -order

        ndigits = max(ndigits, 1)

        factor = 10 ** ndigits

        rounded_error = math.ceil(round(error * factor, 10)) / factor

        rounded_value = round(value, ndigits)

    if toText:
        str_val = f"{rounded_value:.{ndigits}f}".replace(".", ",")
        str_err = f"{rounded_error:.{ndigits}f}".replace(".", ",")
        return f"({str_val} ± {str_err})"

    return rounded_value, rounded_error
