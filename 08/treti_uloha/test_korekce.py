import re
import numpy as np


def round_value_and_error(value, delta):
    """
    Zaokrouhlí chybu podle pravidel (1 nebo 2 platné číslice)
    a naměřenou hodnotu zaokrouhlí na stejný desetinný řád.
    """
    if delta == 0:
        return value, 0.0, 0

    exponent = int(np.floor(np.log10(abs(delta))))
    rounded_1 = round(delta, -exponent)

    s = f"{rounded_1:.10f}"
    first_digit = None
    for char in s:
        if char.isdigit() and char != '0':
            first_digit = int(char)
            break

    if first_digit is not None and first_digit <= 1:
        decimal_places = -exponent + 1
    else:
        decimal_places = -exponent

    final_delta = round(delta, decimal_places)
    final_value = round(value, decimal_places)

    return final_value, final_delta, decimal_places


# Vstupní LaTeX kód tabulky
latex_data = r"""
\begin{tabular}{@{}cccc@{}}
\toprule
$X\,[\mathrm{-}]$ & $Y\,[\mathrm{-}]$ & $\varphi_1\,[\mathrm{V}]$ & $\varphi_2\,[\mathrm{V}]$ \\ \midrule
12                & 1                 & 0,75                      & 8,42                      \\
12                & 2                 & 0,92                      & 8,5                       \\
12                & 3                 & 1,07                      & 8,69                      \\
12                & 4                 & 1,24                      & 8,78                      \\
12                & 5                 & 1,34                      & 8,89                      \\
12                & 6                 & 1,42                      & 8,94                      \\
12                & 7                 & 1,36                      & 8,9                       \\
12                & 8                 & 1,29                      & 8,91                      \\
12                & 9                 & 1,19                      & 8,74                      \\
12                & 10                & 1,07                      & 8,65                      \\
12                & 11                & 0,92                      & 8,4                       \\
12                & 12                & 0,72                      & 8,12                      \\ \bottomrule
\end{tabular}
"""

modified_latex = latex_data

tabular_match = re.search(r'(\\begin\{tabular\}.*?\\end\{tabular\})', latex_data, re.DOTALL)
if tabular_match:
    tabular_block = tabular_match.group(1)
    lines = tabular_block.strip().split('\n')

    new_tabular_lines = []

    for line in lines:
        if any(cmd in line for cmd in ['\\begin', '\\end', '\\toprule', '\\midrule', '$X$']):
            new_tabular_lines.append(line)
            continue

        clean_line = line.replace(r'\\', '').strip()
        if not clean_line:
            new_tabular_lines.append(line)
            continue

        cells = [c.strip() for c in clean_line.split('&')]

        if len(cells) >= 4:
            x_val = cells[0]
            y_val = cells[1]

            raw_val1 = re.sub(r'\\[a-zA-Z]+', '', cells[2]).strip()
            raw_val2 = re.sub(r'\\[a-zA-Z]+', '', cells[3]).strip()

            val1 = float(raw_val1.replace(',', '.'))
            val2 = float(raw_val2.replace(',', '.'))

            # Výpočet přístrojové chyby (rozsah 20 V)
            raw_err1 = 0.005 * val1 + 0.08
            raw_err2 = 0.005 * val2 + 0.08

            # Zaokrouhlení
            r_val1, r_err1, dec1 = round_value_and_error(val1, raw_err1)
            r_val2, r_err2, dec2 = round_value_and_error(val2, raw_err2)

            # Formátování s čárkou, obalením v $...$ a zápisem ±
            str_cell1 = f"${r_val1:.{dec1}f}".replace('.', ',') + r" \pm " + f"{r_err1:.{dec1}f}".replace('.',
                                                                                                          ',') + "$"
            str_cell2 = f"${r_val2:.{dec2}f}".replace('.', ',') + r" \pm " + f"{r_err2:.{dec2}f}".replace('.',
                                                                                                          ',') + "$"

            ending = r" \\ \bottomrule" if "bottomrule" in line else r" \\"

            new_line = f"    {x_val:<17} & {y_val:<17} & {str_cell1:<27} & {str_cell2:<27} {ending}"
            new_tabular_lines.append(new_line)
        else:
            new_tabular_lines.append(line)

    new_tabular_block = "\n".join(new_tabular_lines)
    modified_latex = modified_latex.replace(tabular_block, new_tabular_block)

    print("Změněný LaTeX kód tabulky:\n")
    print(modified_latex)
else:
    print("Tabulka nebyla nalezena.")