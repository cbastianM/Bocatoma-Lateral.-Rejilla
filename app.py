import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import numpy as np

st.set_page_config(page_title="Diseño de Rejilla — Bocatoma Lateral", page_icon="🌊", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:#0d1117;color:#e6edf3;}
h1,h2,h3,h4{font-family:'JetBrains Mono',monospace!important;color:#58a6ff!important;}

.result-box{background:#0d2818;border:1px solid #1a4d2e;border-left:4px solid #3fb950;
            border-radius:8px;padding:10px 14px;margin:8px 0;text-align:center;}
.result-val{font-family:'JetBrains Mono',monospace;font-size:16px;color:#3fb950;font-weight:700;}

.param-box{background:#1a1d2e;border:1px solid #30363d;border-left:4px solid #f6ad55;
           border-radius:8px;padding:8px 12px;margin:4px 0;font-family:'JetBrains Mono',monospace;
           font-size:11px;color:#f6ad55;line-height:1.7;}

.note{color:#8b949e;font-size:12px;font-style:italic;margin:4px 0 8px 0;}

.warn-box{background:#2d1216;border:1px solid #5c2029;border-left:4px solid #f85149;
          border-radius:8px;padding:8px 12px;margin:6px 0;font-family:'JetBrains Mono',monospace;
          font-size:12px;color:#f85149;}
.good-box{background:#0d2818;border:1px solid #1a4d2e;border-left:4px solid #3fb950;
          border-radius:8px;padding:8px 12px;margin:6px 0;font-family:'JetBrains Mono',monospace;
          font-size:12px;color:#3fb950;}

div[data-testid="stSidebar"]{background:#0d1117;border-right:1px solid #21262d;}
footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

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

# Ancho total de la rejilla
ancho_reja = n_varillas * w_bar + n_esp * b_sep

# ════════════════════════════════════════
# PASO 1
# ════════════════════════════════════════
with st.expander("**Paso 1** — Caudal de diseño", expanded=True):

    st.latex(rf"CMD = {CMD} \;\text{{L/s}}")

    st.latex(rf"Q_{{\text{{diseño}}}} = {factor_seg} \times {CMD} = {Q_diseño:.2f} \;\text{{L/s}}")

    st.markdown(f'<div class="result-box"><span class="result-val">Q diseño = {round(Q_diseño)} L/s = {Q_m3s:.6f} m³/s</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# PASO 2
# ════════════════════════════════════════
with st.expander("**Paso 2** — Pérdida de carga en la rejilla (Kirschmer)"):

    st.latex(rf"h_v = {hv:.6f} \;m")

    st.latex(rf"h = {h_kirsch:.6f} \;m")

# ════════════════════════════════════════
# PASO 3
# ════════════════════════════════════════
with st.expander("**Paso 3** — Vertedero sumergido (Villamonte)"):

    st.latex(rf"S = {S:.3f}")

    st.latex(rf"Q_1 = {Q1:.6f} \;m^3/s")

# ════════════════════════════════════════
# PASO 4
# ════════════════════════════════════════
with st.expander("**Paso 4** — Longitud efectiva (Francis)"):

    st.latex(rf"L_e = {Le:.3f} \;m")

# ════════════════════════════════════════
# PASO 5
# ════════════════════════════════════════
with st.expander("**Paso 5** — Número de espacios y varillas"):

    st.latex(rf"N_{{esp}} = {n_esp}")

    st.latex(rf"N_{{var}} = {n_varillas}")

# ════════════════════════════════════════
# PASO 6
# ════════════════════════════════════════
with st.expander("**Paso 6** — Ancho total de la rejilla"):

    st.latex(rf"\text{{Ancho}} = {ancho_reja:.4f} \;m")

# ════════════════════════════════════════
# RESUMEN
# ════════════════════════════════════════
st.markdown("### 📊 Resumen")

st.latex(rf"""
\begin{{array}}{{|l|r|}}
\hline
CMD & {round(CMD)} \;\text{{L/s}} \\
Q_{{\text{{diseño}}}} & {round(Q_diseño)} \;\text{{L/s}} \\
\hline
S & {round(S,2)} \\
Q_1 & {round(Q1,3)} \;\text{{m³/s}} \\
\hline
L_e & {round(Le,2)} \;\text{{m}} \\
\hline
N°\text{{esp}} & {n_esp} \\
N°\text{{var}} & {n_varillas} \\
\text{{Ancho rejilla}} & {ancho_reja:.4f} \;\text{{m}} \\
\hline
\end{{array}}
""")
