import argparse
import re
import sys
import tkinter as tk

import sympy as sp


def spocti_parcialni_derivace(vzorec_str, ignorovat=[]):
  vzorec_str = vzorec_str.replace("^", "**")
  expr = sp.sympify(vzorec_str)
  vsechny_symboly = expr.free_symbols
  ignorovat_set = {sp.Symbol(v) for v in ignorovat}
  cilove_promenne = sorted(
      [s for s in vsechny_symboly if s not in ignorovat_set], key=str
  )

  vysledky = {}
  for var in cilove_promenne:
    vysledky[var] = sp.diff(expr, var)

  return expr, vysledky


def formatuj_pro_sheets(vyraz):
  """Převede jednotlivý SymPy výraz (derivaci) do čistého textu pro Google Sheets."""
  s = str(vyraz)
  s = s.replace("**", "^")
  s = s.replace("sqrt", "ODMOCNINA")
  s = s.replace("*", " * ")
  s = s.replace("/", " / ")
  return re.sub(r"\s+", " ", s)


def neprima_chyba(vzorec_str, ignorovat=[]):
  expr, derivace_dict = spocti_parcialni_derivace(vzorec_str, ignorovat)

  clenove_pod_odmocninou = 0
  latex_sum_items = []
  sheets_sum_items = []

  for var, derivace in derivace_dict.items():
    sig = sp.Symbol(f"sigma_{var}")

    clen = (derivace * sig) ** 2
    clenove_pod_odmocninou += clen

    latex_sum_items.append(f"\\left( ({sp.latex(derivace)}) \\cdot \\sigma_{var} \\right)^2")

    der_sheets = formatuj_pro_sheets(derivace)
    sheets_sum_items.append(f"(({der_sheets}) * sigma_{var})^2")

  celkova_chyba = sp.sqrt(clenove_pod_odmocninou)

  latex_vysledek = (
      f"$$ \\sigma_f = \\sqrt{{ " + " + ".join(latex_sum_items) + " }} $$"
  )
  print("=== LaTeX výstup ===")
  print(latex_vysledek)
  print("\n" + "=" * 40 + "\n")

  sheets_vzorec = "=ODMOCNINA(" + " + ".join(sheets_sum_items) + ")"
  print("=== Google Sheets vzorec (česky) ===")
  print(sheets_vzorec)
  print("")

  return celkova_chyba, latex_vysledek, sheets_vzorec


def open_copy_window(latex_rovnice, latex_vzorec, sheets_str):
  """Otevře okno s náhledem originální rovnice a tlačítky pro kopírování výsledků."""
  root = tk.Tk()
  root.title("Kopírování vzorců")
  root.geometry("400x230")
  root.eval("tk::PlaceWindow . center")

  def copy_text(text, label_name):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    status_label.config(text=f"Zkopírováno: {label_name}!")

  lbl_title = tk.Label(
      root, text=f"Originální rovnice:", font=("Arial", 10, "bold")
  )
  lbl_title.pack(pady=(12, 2))

  lbl_rovnice = tk.Label(
      root,
      text=latex_rovnice,
      font=("Consolas", 11),
      fg="#333333",
      wraplength=380,
  )
  lbl_rovnice.pack(pady=(0, 10))

  btn_eq = tk.Button(
      root,
      text="Copy LaTeX (Originální rovnice)",
      width=32,
      command=lambda: copy_text(latex_rovnice, "LaTeX (Originální rovnice)"),
  )
  btn_eq.pack(pady=3)

  btn_latex = tk.Button(
      root,
      text="Copy LaTeX (Celková chyba)",
      width=32,
      command=lambda: copy_text(latex_vzorec, "LaTeX (Celková chyba)"),
  )
  btn_latex.pack(pady=3)

  btn_sheets = tk.Button(
      root,
      text="Copy Google Sheets",
      width=32,
      command=lambda: copy_text(sheets_str, "Google Sheets"),
  )
  btn_sheets.pack(pady=3)

  status_label = tk.Label(root, text="", fg="green", font=("Arial", 9))
  status_label.pack(pady=(5, 0))

  root.mainloop()

# ==========================================
#  Použití např.: :
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process pro výpočet nepřímé chyby a převod do LaTeXu a Google Sheets.")
    parser.add_argument(
        "rovnice",
        nargs="+",
        type=str,
        help="Rovnice pro kterou to poběží (např. '1/2 * m * r^2')",
    )
    parser.add_argument(
        "-i",
        "--ignorovat",
        nargs="*",
        default=[],
        type=str,
        help="Seznam proměnných, které se mají ignorovat (považovat za konstanty)",
    )

    args = parser.parse_args()

    for rovnice_str in args.rovnice:
        sym_vysledek, latex_vzorec, sheets_vzorec = neprima_chyba(rovnice_str, ignorovat=args.ignorovat)
        open_copy_window(rovnice_str, latex_vzorec, sheets_vzorec)