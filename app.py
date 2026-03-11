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

details summary{font-family:'JetBrains Mono',monospace;font-size:13px;cursor:pointer;color:#58a6ff;}

/* Márgenes laterales para bloques matemáticos */
.stMarkdown .katex-display{margin-left:1.5rem!important;margin-right:1.5rem!important;}
div[data-testid="stExpander"]{padding-left:0.5rem;padding-right:0.5rem;}
div[data-testid="stExpander"] .katex-display{margin-left:1rem!important;margin-right:1rem!important;}

/* Eliminar scrollbars en bloques matemáticos */
.katex-display{overflow:visible!important;overflow-x:visible!important;}
.katex-display>.katex{overflow:visible!important;overflow-x:visible!important;}
.katex-display>.katex>.katex-html{overflow:visible!important;overflow-x:visible!important;}
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"]{overflow:visible!important;}
.element-container{overflow:visible!important;}
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
perdida_norma = 0.10  # por norma: 10 cm
perdida = max(h_kirsch, perdida_norma)

S  = (H_carga - perdida) / H_carga
Q1 = Q_m3s / (1 - S**1.5)**0.385

Le = Q1 / (1.84 * H_carga**1.5)

d_var      = w_bar
espacios   = Le / d_var
n_esp      = round(espacios)
n_varillas = n_esp - 1

Lv = (Q1 / (1.86 * H_carga**1.6))**(1 / 0.9)

# Ancho total de la rejilla
ancho_reja = n_varillas * w_bar + n_esp * b_sep

# ══════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════
st.markdown("# 🌊 Diseño de Rejilla")
st.markdown("##### Bocatoma Lateral — Procedimiento paso a paso")

st.latex(rf"""
\begin{{aligned}}
\textbf{CMD} &= {CMD} \;\text{L/s} \\
\text{Factor} &= {factor_seg} \\
\textbf{{Varilla}} &: \text{{{tipo_varilla.split('(')[0].strip()}}} \;\; \phi \, {d_varilla_pulg}\text{{''}} \\
w \;\text{{(espesor)}} &= {w_bar*100:.2f} \;\text{{cm}} \;=\; {d_varilla_pulg}\text{{''}} \\
b \;\text{{(separación libre)}} &= {b_sep*100:.2f} \;\text{{cm}} \;=\; {sep_pulg}\text{{''}} \\
\alpha &= {angulo_rej}° \\
v &= {v_aprox} \;\text{{m/s}} \\
H &= {H_carga} \;\text{{m}}
\end{{aligned}}
""")

st.markdown("")

# ════════════════════════════════════════
# PASO 1
# ════════════════════════════════════════
with st.expander("**Paso 1** — Caudal de diseño", expanded=True):
    st.markdown(f'<p class="note">Se usa {factor_seg}·CMD por seguridad.</p>', unsafe_allow_html=True)

    st.latex(rf"CMD = {CMD} \;\text{{L/s}}")

    st.latex(rf"Q_{{\text{{diseño}}}} = {factor_seg} \times CMD = {factor_seg} \times {CMD:.2f} = {Q_diseño:.2f} \;\text{{L/s}}")

    st.markdown(f'<div class="result-box"><span class="result-val">Q diseño = {round(Q_diseño)} L/s = {Q_m3s:.6f} m³/s</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# PASO 2
# ════════════════════════════════════════
with st.expander("**Paso 2** — Pérdida de carga en la rejilla (Kirschmer)"):
    st.markdown(f'<p class="note">B={B_factor} · w={w_bar:.4f} m · b={b_sep:.4f} m · v={v_aprox} m/s · α={angulo_rej}°</p>', unsafe_allow_html=True)

    st.latex(rf"h_v = \frac{{v^2}}{{2g}} = \frac{{{v_aprox}^2}}{{2(9.81)}} = \boxed{{{hv:.6f} \;\text{{m}}}}")

    st.latex(r"h = B \left(\frac{w}{b}\right)^{\!4/3} \!\cdot h_v \cdot \sin\alpha")

    st.latex(rf"h = {B_factor} \left(\frac{{{w_bar:.4f}}}{{{b_sep:.4f}}}\right)^{{\!4/3}} \!\cdot {hv:.6f} \cdot \sin {angulo_rej}°")

    st.latex(rf"h = {B_factor} \times {(w_bar/b_sep)**(4/3):.4f} \times {hv:.6f} \times {math.sin(ang_rad):.4f}")
    st.latex(rf"\boxed{{h = {h_kirsch:.6f} \;\text{{m}} = {h_kirsch*100:.4f} \;\text{{cm}}}}")

    st.markdown("**Pérdida (por norma: mínimo 10 cm):**")
    if h_kirsch > perdida_norma:
        st.latex(rf"h = {h_kirsch*100:.4f} \;\text{{cm}} > 10 \;\text{{cm}} \;\;\Rightarrow\;\; \text{{se toma }} h")
    else:
        st.latex(rf"h = {h_kirsch*100:.4f} \;\text{{cm}} < 10 \;\text{{cm}} \;\;\Rightarrow\;\; \text{{se toma 10 cm (norma)}}")

    st.markdown(f'<div class="result-box"><span class="result-val">Pérdida de carga = {perdida:.2f} m = {perdida*100:.1f} cm</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# PASO 3
# ════════════════════════════════════════
with st.expander("**Paso 3** — Vertedero sumergido (Villamonte)"):
    st.markdown(f'<p class="note">Corrección del caudal por sumergencia.</p>', unsafe_allow_html=True)

    st.latex(rf"S = \frac{{H - 3h}}{{H}} = \frac{{{H_carga} - {perdida}}}{{{H_carga}}} = \boxed{{{S:.4f} \approx {round(S,2)}}}")

    st.latex(r"Q_1 = \frac{Q}{\left(1 - S^{1.5}\right)^{0.385}}")

    st.latex(rf"Q_1 = \frac{{{Q_m3s:.6f}}}{{\left(1 - {S:.4f}^{{1.5}}\right)^{{0.385}}}}")
    st.latex(rf"Q_1 = \frac{{{Q_m3s:.6f}}}{{{(1 - S**1.5)**0.385:.6f}}} = \boxed{{{Q1:.6f} \;\text{{m³/s}}}}")

    st.markdown(f'<div class="result-box"><span class="result-val">Q₁ = {round(Q1,3)} m³/s</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# PASO 4
# ════════════════════════════════════════
with st.expander("**Paso 4** — Longitud efectiva (Francis)"):
    st.markdown(f'<p class="note">Longitud del vertedero para captar Q₁.</p>', unsafe_allow_html=True)

    st.latex(r"L_e = \frac{Q_1}{1.84 \cdot H^{3/2}}")

    st.latex(rf"L_e = \frac{{{Q1:.6f}}}{{1.84 \times {H_carga}^{{3/2}}}}")
    st.latex(rf"L_e = \frac{{{Q1:.6f}}}{{{1.84 * H_carga**1.5:.6f}}} = \boxed{{{Le:.4f} \;\text{{m}}}}")

    st.markdown(f'<div class="result-box"><span class="result-val">Le = {Le:.4f} m ≈ {round(Le,2)} m</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# PASO 5
# ════════════════════════════════════════
with st.expander("**Paso 5** — Número de espacios y varillas"):
    st.markdown(f'<p class="note">d = Ø varilla = {w_bar:.4f} m = {w_bar*100:.2f} cm</p>', unsafe_allow_html=True)

    st.latex(rf"N_{{\text{{esp}}}} = \frac{{L_e}}{{d}} = \frac{{{Le:.4f}}}{{{w_bar:.4f}}}")
    st.latex(rf"N_{{\text{{esp}}}} = {espacios:.2f} \approx \boxed{{{n_esp}}}")

    st.latex(rf"N_{{\text{{var}}}} = N_{{\text{{esp}}}} - 1 = {n_esp} - 1 = \boxed{{{n_varillas}}}")

    st.markdown(f'<div class="result-box"><span class="result-val">{n_esp} espacios · {n_varillas} varillas</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════
# PASO 6
# ════════════════════════════════════════
with st.expander("**Paso 6** — Ancho total de la rejilla"):
    st.markdown(f'<p class="note">Separación libre entre varillas: b = {b_sep*100:.2f} cm = {sep_pulg}"</p>', unsafe_allow_html=True)

    st.latex(r"\text{Ancho} = N_{\text{var}} \cdot w \;+\; N_{\text{esp}} \cdot b")

    st.latex(rf"\text{{Ancho}} = {n_varillas} \times {w_bar:.4f} + {n_esp} \times {b_sep:.4f}")

    st.latex(rf"\text{{Ancho}} = {n_varillas * w_bar:.4f} + {n_esp * b_sep:.4f}")

    st.markdown(f'<div class="result-box"><span class="result-val">Ancho rejilla = {ancho_reja:.4f} m = {ancho_reja*100:.2f} cm</span></div>', unsafe_allow_html=True)

    st.markdown(f'<p class="note">Varillas: {n_varillas} × {w_bar*100:.2f} cm = {n_varillas*w_bar*100:.2f} cm<br>Espacios: {n_esp} × {b_sep*100:.2f} cm = {n_esp*b_sep*100:.2f} cm</p>', unsafe_allow_html=True)

# ════════════════════════════════════════
# RESUMEN
# ════════════════════════════════════════
st.markdown("---")
st.markdown("### 📊 Resumen")

st.latex(rf"""
\begin{{array}}{{|l|r|}}
\hline
CMD & {round(CMD)} \;\text{{L/s}} \\
Q_{{\text{{diseño}}}} & {round(Q_diseño)} \;\text{{L/s}} \\
\hline
3h & {perdida:.2f} \;\text{{m}} \\
S & {round(S,2)} \\
Q_1 & {round(Q1,3)} \;\text{{m³/s}} \\
\hline
L_e & {round(Le,2)} \;\text{{m}} \\
L_v & {round(Lv,2)} \;\text{{m}} \\
\hline
N°\text{{esp}} & {n_esp} \\
N°\text{{var}} & {n_varillas} \\
\text{{Ancho rejilla}} & {ancho_reja:.4f} \;\text{{m}} \\
\hline
\end{{array}}
""")

st.markdown("---")
st.markdown("### 🔩 Representación de la Rejilla")

# ── Gráfico de la rejilla ──
# Escala en centímetros para visibilidad
ancho_cm = ancho_reja * 100
d_cm     = w_bar * 100
b_cm     = b_sep * 100   # separación libre en cm
H_dibujo = 100.0  # altura fija = 1 m = 100 cm

CBG = '#0d1117'
fig, ax = plt.subplots(figsize=(14, 4))
fig.patch.set_facecolor(CBG)
ax.set_facecolor('#0a0e14')
ax.tick_params(colors='#4a5568', labelsize=7, direction='in')
for sp in ax.spines.values():
    sp.set_color('#21262d')

# Marco exterior
marco_t = d_cm * 1.2
ax.add_patch(plt.Rectangle(
    (-marco_t, -marco_t), ancho_cm + 2*marco_t, H_dibujo + 2*marco_t,
    lw=2, ec='#7a8fa3', fc='#141a22', zorder=1))

# Fondo (espacio libre)
ax.add_patch(plt.Rectangle(
    (0, 0), ancho_cm, H_dibujo,
    lw=1.2, ec='#7a8fa3', fc='#0a0e14', zorder=2))

# Varillas: b | w | b | w | b | ... | b
# Primera separación, luego alternan varilla-separación
for i in range(n_varillas):
    x_left = b_cm + i * (d_cm + b_cm)
    if x_left + d_cm > ancho_cm:
        break
    ax.add_patch(plt.Rectangle(
        (x_left, 0), d_cm, H_dibujo,
        lw=0, fc='#6c5ce7', alpha=0.85, zorder=3))

# ── Acotado ──
# Ancho total (abajo)
y_dim = -marco_t - 6
ax.annotate("", xy=(ancho_cm, y_dim), xytext=(0, y_dim),
            arrowprops=dict(arrowstyle='<->', color='#f6e05e', lw=1))
ax.text(ancho_cm/2, y_dim - 3,
        f'Ancho rejilla = {ancho_reja:.4f} m ({ancho_cm:.2f} cm)',
        ha='center', va='top', color='#f6e05e', fontsize=9,
        fontfamily='monospace', fontweight='bold')

# Altura (derecha)
x_dim = ancho_cm + marco_t + 4
ax.annotate("", xy=(x_dim, H_dibujo), xytext=(x_dim, 0),
            arrowprops=dict(arrowstyle='<->', color='#f6e05e', lw=1))
ax.text(x_dim + 3, H_dibujo/2, '1.00 m',
        ha='left', va='center', color='#f6e05e', fontsize=8,
        fontfamily='monospace', rotation=90)

# Detalle ampliado (3 varillas + 2 espacios)
# Dibujado en una caja aparte arriba a la derecha
det_x0 = ancho_cm * 0.55
det_y0 = H_dibujo * 0.35
det_w  = ancho_cm * 0.42
det_h  = H_dibujo * 0.55

ax.add_patch(mpatch.FancyBboxPatch(
    (det_x0, det_y0), det_w, det_h,
    boxstyle=mpatch.BoxStyle.Round(pad=1),
    lw=1.5, ec='#58a6ff', fc='#0d1117', alpha=0.95, zorder=10))
ax.text(det_x0 + det_w/2, det_y0 + det_h - 3, 'DETALLE',
        ha='center', va='top', color='#58a6ff', fontsize=7,
        fontfamily='monospace', fontweight='bold', zorder=11)

# 3 varillas ampliadas
n_det = 3
total_det = n_det * d_cm + (n_det + 1) * b_cm
scale = det_w * 0.55 / total_det if total_det > 0 else 1
d_s = d_cm * scale
b_s = b_cm * scale

det_vbase = det_y0 + det_h * 0.28
det_vtop  = det_y0 + det_h * 0.65
det_vh    = det_vtop - det_vbase
x_start   = det_x0 + (det_w - (n_det * d_s + (n_det + 1) * b_s)) / 2

for i in range(n_det):
    vx = x_start + b_s + i * (d_s + b_s)
    ax.add_patch(plt.Rectangle(
        (vx, det_vbase), d_s, det_vh,
        lw=0.5, ec='#5a4fcf', fc='#6c5ce7', alpha=0.9, zorder=11))

# Acotado b (solo en el primer espacio, entre varilla 1 y 2)
vx1_right = x_start + b_s + d_s                    # borde derecho varilla 1
vx2_left  = x_start + b_s + (d_s + b_s)            # borde izquierdo varilla 2
mid_b = (vx1_right + vx2_left) / 2
yd_b = det_vbase - 4
ax.annotate("", xy=(vx2_left, yd_b), xytext=(vx1_right, yd_b),
            arrowprops=dict(arrowstyle='<->', color='#3fb950', lw=0.8), zorder=11)
ax.text(mid_b, yd_b - 6.5, f'b = {b_sep*100:.2f} cm',
        ha='center', color='#3fb950', fontsize=6.5,
        fontfamily='monospace', fontweight='bold', zorder=11)

# Acotado d (sobre la primera varilla)
vx0 = x_start + b_s
yd_top = det_vtop + 3
ax.annotate("", xy=(vx0 + d_s, yd_top), xytext=(vx0, yd_top),
            arrowprops=dict(arrowstyle='<->', color='#9f7aea', lw=0.8), zorder=11)
ax.text(vx0 + d_s/2, yd_top + 3.5, f'w = {d_cm:.2f} cm',
        ha='center', color='#9f7aea', fontsize=6.5,
        fontfamily='monospace', fontweight='bold', zorder=11)

# Info
ax.text(ancho_cm * 0.22, H_dibujo * 0.5,
        f'{n_varillas} varillas\n{n_esp} espacios',
        ha='center', va='center', color='#e2e8f0', fontsize=9,
        fontfamily='monospace', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', fc='#161b22', ec='#30363d', alpha=0.9),
        zorder=10)

ax.set_xlim(-marco_t - 8, ancho_cm + marco_t + 18)
ax.set_ylim(-marco_t - 16, H_dibujo + marco_t + 6)
ax.set_aspect('equal')
ax.set_xlabel("cm", color='#636e72', fontsize=7, fontfamily='monospace')
ax.set_ylabel("cm", color='#636e72', fontsize=7, fontfamily='monospace')
ax.set_title('REJILLA', color='#e2e8f0', fontsize=10,
             fontfamily='monospace', pad=8)

plt.tight_layout(pad=0.8)
st.pyplot(fig)
plt.close(fig)

st.markdown(
    '<p style="text-align:center;color:#4a5568;font-family:JetBrains Mono,monospace;'
    'font-size:10px;margin-top:12px;">'
    'Bocatoma Lateral · Kirschmer · Villamonte · Francis</p>',
    unsafe_allow_html=True)
