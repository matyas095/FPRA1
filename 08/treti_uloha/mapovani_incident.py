import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Pevné souřadnice X a Y (1 až 12)
x = np.arange(1, 13)
y = np.arange(1, 13)
X, Y = np.meshgrid(x, y)

# 2. Vstupní data
phi_1_vals = np.array([
    0.7, 0.89, 1.06, 1.22, 1.3, 1.36, 1.4, 1.35, 1.22, 1.1, 0.93, 0.78, 0.93, 1.14, 1.36, 1.5, 1.65, 1.78, 1.76, 1.71, 1.52, 1.38, 1.13, 0.87, 1.05, 1.29, 1.51, 1.75, 1.98, 2.17, 2.16, 2.1, 1.83, 1.59, 1.29, 1.1, 1.16, 1.4, 1.71, 2.02, 2.37, 2.64, 2.72, 2.5, 2.16, 1.87, 1.53, 1.22, 1.28, 1.52, 1.87, 2.27, 2.77, 3.4, 3.59, 3.07, 2.59, 2.05, 1.67, 1.32, 1.28, 1.61, 2.02, 2.58, 3.34, 4.21, 4.73, 3.63, 2.88, 2.2, 1.75, 1.34, 1.24, 1.57, 1.93, 2.42, 3.05, 4.34, 4.19, 3.14, 2.49, 1.98, 1.55, 1.21, 1.18, 1.48, 1.86, 2.28, 2.85, 3.25, 3.25, 2.83, 2.3, 1.87, 1.49, 1.21, 1.14, 1.4, 1.7, 2, 2.36, 2.65, 2.59, 2.36, 2.03, 1.73, 1.37, 1.14, 1.05, 1.33, 1.55, 1.79, 2.03, 2.17, 2.12, 2.01, 1.75, 1.5, 1.26, 1.02, 0.88, 1.09, 1.29, 1.49, 1.65, 1.66, 1.75, 1.61, 1.46, 1.25, 1.07, 0.85, 0.75, 0.92, 1.07, 1.24, 1.34, 1.42, 1.36, 1.29, 1.19, 1.07, 0.92, 0.72
])

phi_2_vals = np.array([
    1.8, 1.6, 1.51, 1.43, 1.41, 1.36, 1.35, 1.43, 1.53, 1.65, 1.85, 2.1, 1.61, 1.42, 1.28, 1.2, 1.19, 1.22, 1.22, 1.6, 1.39, 1.53, 1.88, 2.14, 1.42, 1.15, 1.04, 1.01, 1, 1.04, 1.03, 1.05, 1.15, 1.4, 1.81, 2.27, 1.18, 0.9, 0.83, 0.85, 0.88, 0.89, 0.86, 0.84, 0.85, 1.16, 1.8, 2.56, 2.12, 2.7, 2.37, 2.26, 2.8, 2.82, 2.01, 2.06, 2.04, 2.29, 3.59, 4.03, 3.7, 3.1, 2.8, 2.91, 3.26, 3.14, 2.97, 2.67, 2.85, 2.98, 3.27, 4.3, 5.73, 7.01, 7.6, 7.2, 7.25, 7.19, 7.7, 8.93, 8.2, 8.08, 6.05, 5.81, 8.32, 9.04, 8.99, 8.95, 9.04, 9.12, 9.3, 9.41, 9.45, 9.48, 9.43, 8.76, 8.04, 8.6, 8.8, 8.88, 9.02, 9.09, 9.24, 9.43, 9.4, 9.2, 8.71, 7.98, 8.33, 8.66, 8.8, 9.01, 9.05, 9.15, 9.35, 9.18, 9.24, 9.05, 8.66, 8.23, 8.28, 8.55, 8.7, 8.8, 8.95, 9.01, 9.1, 9.06, 9.06, 8.89, 8.59, 8.23, 8.42, 8.5, 8.69, 8.78, 8.89, 8.94, 8.9, 8.91, 8.74, 8.65, 8.4, 8.12
])

Z1 = phi_1_vals.reshape(12, 12)
Z2 = phi_2_vals.reshape(12, 12)

# Vytvoření subplotů s 3D scénami vedle sebe
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scene'}, {'type': 'scene'}]],
    subplot_titles=('Konfigurace 1 ($\varphi_1$)', 'Konfigurace 2 ($\varphi_2त्र$)'.replace('त्र', ''))
)

# Přidání povrchu pro 1. konfiguraci
fig.add_trace(
    go.Surface(z=Z1, x=X, y=Y, colorscale='Viridis', colorbar=dict(x=0.42, len=0.75), name='Konf. 1'),
    row=1, col=1
)

# Přidání povrchu pro 2. konfiguraci
fig.add_trace(
    go.Surface(z=Z2, x=X, y=Y, colorscale='Plasma', colorbar=dict(x=1.0, len=0.75), name='Konf. 2'),
    row=1, col=2
)

# Úprava vzhledu a popisků os
fig.update_layout(
    title_text="Interaktivní 3D mapování elektrostatického pole",
    scene=dict(xaxis_title='X [-]', yaxis_title='Y [-]', zaxis_title='φ₁ [V]'),
    scene2=dict(xaxis_title='X [-]', yaxis_title='Y [-]', zaxis_title='φ₂ [V]'),
    width=1400,
    height=700
)

# Otevření v prohlížeči a uložení jako interaktivní HTML
fig.show()
fig.write_html('interaktivni_potencialy.html')
print("Interaktivní graf byl uložen do souboru 'interaktivni_potencialy.html'.")