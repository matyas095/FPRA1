import math


def round_val_err(value, error, toText=False):
    value = float(value)
    error = float(error)

    if error <= 0:
        ndigits = 1
        rounded_error = round(error, ndigits)
        rounded_value = round(value, ndigits)
    else:
        if error >= 1:
            integer_part = math.floor(error)
            frac = error - integer_part
            first_decimal = math.floor(frac * 10)
            if first_decimal == 1:
                ndigits = 2
            else:
                ndigits = 1
        else:
            order = math.floor(math.log10(error))
            leading_digit = math.floor(error / (10 ** order))
            if leading_digit == 1 and order == -1:
                ndigits = 2
            else:
                ndigits = max(-order - 1, 1)

        factor = 10 ** ndigits
        rounded_error = math.ceil(round(error * factor, 10)) / factor
        rounded_value = round(value, ndigits)

    if toText:
        precision = max(ndigits, 0)
        str_val = f"{rounded_value:.{precision}f}".replace(".", ",")
        str_err = f"{rounded_error:.{precision}f}".replace(".", ",")
        return f"({str_val} ± {str_err})"

    return rounded_value, rounded_error


if __name__ == "__main__":
    print(round_val_err(7.6, 2.14362479, toText=True))  # (7,6 ± 2,15)
    print(round_val_err(0.5, 0.1434, toText=True))      # (0,5 ± 0,15)
    print(round_val_err(0.5, 0.2434, toText=True))      # (0,5 ± 0,3)
    print(round_val_err(0.5, 0.0434, toText=True))      # (0,5 ± 0,1)
    print(round_val_err(0.002605, 0.000731, toText=True))  # (0,003 ± 0,001)