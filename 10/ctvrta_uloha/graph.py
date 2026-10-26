import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

from scipy.optimize import curve_fit

script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "outputs"
subfolders = sorted(
    [f for f in data_dir.iterdir() if f.is_dir()], key=lambda f: f.name
)