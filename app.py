import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import numpy as np

st.set_page_config(page_title="Diseño de Rejilla — Bocatoma Lateral", page_icon="🌊", layout="centered")

# ══════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Datos de Entrada")

    st.markdown("#### Caudal de diseño")
    CMD = st.number_input("Caudal Máximo Diario CMD (L/s)", value=120.0, step=1.0)
    factor_seg = st.selectbox("Factor de seguridad", [3,2], index=0)

    st.markdown("#### Rejilla")
    tipo_varilla   = st.selectbox("Sección varilla", ["Circular (B=1.79)", "Rectangular (B=2.42)"])
    B_factor       = 1.79 if "Circular" in tipo_varilla else 2.42
    d_varilla_pulg = st.selectbox("Ø varilla (pulg)", [1.0, 0.75, 1.25, 1.5])
    w_bar          = d_varilla_pulg * 0.0254
    sep_pulg       = st.selectbox("Separación libre (pulg)", [1.0, 0.75, 1.25, 1.5, 2.0])
    b_sep          = sep_pulg * 0.0254
    angulo_rej     = st.slider("Inclinación α (°)", 45, 80, 60, 5)
    v_aprox        = st.slider("Vel. aproximación v (m/s)", 0.3, 1.0, 0.6, 0.05)

    st.markdown("#### Vertedero")
    H_carga  = st.slider("Carga H sobre cresta (m)", 0.15, 0.80, 0.35, 0.01)

# ══════════════════════════════════════════════════
# CÁLCULOS
# ══════════════════════════════════════════════════
ang_rad = angulo_rej * math.pi / 180
g = 9.81

Q_diseño = factor_seg * CMD
Q_m3s    = Q_diseño / 1000

hv       = v_aprox**2 / (2 * g)
h_kirsch = B_factor * (w_bar / b_sep)**(4/3) * hv * math.sin(ang_rad)

perdida_norma = 0.10
perdida = max(h_kirsch, perdida_norma)

S  = (H_carga - perdida) / H_carga
Q1 = Q_m3s / (1 - S**1.5)**0.385

Le = Q1 / (1.84 * H_carga**1.5)

d_var      = w_bar
espacios   = Le / d_var
n_esp      = round(espacios)
n_varillas = n_esp - 1

ancho_reja = n_varillas * w_bar + n_esp * b_sep

# ══════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════
st.markdown("# 🌊 Diseño de Rejilla")
st.markdown("##### Bocatoma Lateral — Procedimiento paso a paso")

st.latex(rf"""
\begin{{aligned}}
\textbf{{CMD}} &= {CMD} \;\text{{L/s}} \\
\text{{Factor}} &= {factor_seg} \\
\textbf{{Varilla}} &: \text{{{tipo_varilla.split('(')[0].strip()}}} \;\; \phi \, {d_varilla_pulg}\text{{''}} \\
w &= {w_bar*100:.2f} \;\text{{cm}} \\
b &= {b_sep*100:.2f} \;\text{{cm}} \\
\alpha &= {angulo_rej}° \\
v &= {v_aprox} \;\text{{m/s}} \\
H &= {H_carga} \;\text{{m}}
\end{{aligned}}
""")

# ════════════════════════════════════════
# PASO 1
# ════════════════════════════════════════
with st.expander("**Paso 1 — Caudal de diseño**", expanded=True):

    st.latex(rf"CMD = {CMD} \;L/s")

    st.latex(rf"Q_{{diseño}} = {factor_seg} \times CMD")

    st.latex(rf"Q_{{diseño}} = {factor_seg} \times {CMD} = {Q_diseño:.2f} \;L/s")

    st.success(f"Q diseño = {round(Q_diseño)} L/s  ({Q_m3s:.5f} m³/s)")

# ════════════════════════════════════════
# PASO 2
# ════════════════════════════════════════
with st.expander("**Paso 2 — Pérdida de carga en la rejilla (Kirschmer)**"):

    st.latex(rf"h_v = \frac{{v^2}}{{2g}} = {hv:.6f} \;m")

    st.latex(r"h = B \left(\frac{w}{b}\right)^{4/3} h_v \sin \alpha")

    st.latex(rf"h = {h_kirsch:.6f} \;m")

    st.success(f"Pérdida adoptada = {perdida:.2f} m")

# ════════════════════════════════════════
# PASO 3
# ════════════════════════════════════════
with st.expander("**Paso 3 — Vertedero sumergido (Villamonte)**"):

    st.latex(r"S = \frac{H - h}{H}")

    st.latex(rf"S = {S:.3f}")

    st.latex(r"Q_1 = \frac{Q}{(1-S^{1.5})^{0.385}}")

    st.latex(rf"Q_1 = {Q1:.6f} \;m^3/s")

# ════════════════════════════════════════
# PASO 4
# ════════════════════════════════════════
with st.expander("**Paso 4 — Longitud efectiva (Francis)**"):

    st.latex(r"L_e = \frac{Q_1}{1.84H^{3/2}}")

    st.latex(rf"L_e = {Le:.3f} \;m")

# ════════════════════════════════════════
# PASO 5
# ════════════════════════════════════════
with st.expander("**Paso 5 — Número de espacios y varillas**"):

    st.latex(r"N_{esp} = \frac{L_e}{d}")

    st.latex(rf"N_{{esp}} = {espacios:.2f} \approx {n_esp}")

    st.latex(rf"N_{{var}} = {n_varillas}")

# ════════════════════════════════════════
# PASO 6
# ════════════════════════════════════════
with st.expander("**Paso 6 — Ancho total de la rejilla**"):

    st.latex(r"\text{Ancho} = N_{var}w + N_{esp}b")

    st.latex(rf"\text{{Ancho}} = {ancho_reja:.4f} \;m")

    st.success(f"Ancho rejilla = {ancho_reja:.3f} m")

# ════════════════════════════════════════
# RESUMEN
# ════════════════════════════════════════
st.markdown("### 📊 Resumen")

st.latex(rf"""
\begin{{array}}{{|l|r|}}
\hline
CMD & {round(CMD)} \;L/s \\
Q_{{diseño}} & {round(Q_diseño)} \;L/s \\
\hline
S & {round(S,2)} \\
Q_1 & {round(Q1,3)} \;m^3/s \\
\hline
L_e & {round(Le,2)} \;m \\
\hline
N_{{esp}} & {n_esp} \\
N_{{var}} & {n_varillas} \\
Ancho & {ancho_reja:.3f} \;m \\
\hline
\end{{array}}
""")

st.markdown("---")
st.markdown("### 🔩 Representación de la Rejilla")

ancho_cm = ancho_reja * 100
d_cm     = w_bar * 100
b_cm     = b_sep * 100
H_dibujo = 100

fig, ax = plt.subplots(figsize=(14,4))

for i in range(n_varillas):
    x_left = b_cm + i*(d_cm + b_cm)
    ax.add_patch(plt.Rectangle((x_left,0), d_cm, H_dibujo))

ax.set_xlim(0, ancho_cm)
ax.set_ylim(0, H_dibujo)

st.pyplot(fig)
