import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from love_dynamics.interpretation.romantic_styles import RomanticStyleClassifier
from love_dynamics.interpretation.dynamical_interpretation import analyze_dyadic_relationship
from love_dynamics.interpretation.initial_conditions import InitialConditionAnalyzer

st.set_page_config(
    page_title="Love dynamics - Sprott(2004)",
    layout="wide"
)

st.title("Modelos Dinamicos de Relaciones Diadicas")
st.markdown(
    "Plataforma Interactiva basada en el modelo lineal de **J. C. Sprott (2004)** "
    "para el analisis del amor y el odio entre Romeo y Julieta."
)

st.sidebar.subheader("Coeficientes de Romeo")
a = st.sidebar.slider("Reaccion a su propio pasado ($a$)", -2.0, 2.0, 1.0, 0.1)
b = st.sidebar.slider("Reaccion a Julieta ($b$)", -2.0, 2.0, 1.0, 0.1)

st.sidebar.subheader("Coeficientes de Julieta")
c = st.sidebar.slider("Reaccion a Romeo ($c$)", -2.0, 2.0, 1.0, 0.1)
d = st.sidebar.slider("Reaccion a su propio pasado ($d$)", -2.0, 2.0, 1.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.header("Condiciones Iniciales ($t=0$)")
r0 = st.sidebar.slider("Amor inicial de Romeo ($R_0)$)", -5.0, 5.0, 1.0, 0.1)
j0 = st.sidebar.slider("Amor inicial de Julieta ($J_0)$)", -5.0, 5.0, 1.0, 0.1)

romeo_profile = RomanticStyleClassifier.classify(a, b)
juliet_profile = RomanticStyleClassifier.classify(d, c)

st.subheader("Arqueotipos Romanticos Identificiados")
col_r, col_j = st.columns(2)

with col_r:
    st.markdown(f"### Perfil de Romeo")
    st.info(f"**Estilo:** {romeo_profile.category.value}\n\n{romeo_profile.description}")

with col_r:
    st.markdown(f"### Perfil de Julieta")
    st.info(f"**Estilo:** {juliet_profile.category.value}\n\n{juliet_profile.description}")

st.markdown("---")

st.subheader("Analisis Topologico y Estabilidad a Largo Plazo")
analysis = analyze_dyadic_relationship(a=a, b=b, c=c, d=d)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Traza", f"{analysis['trace']:.2f}")
m2.metric("Determinante", f"{analysis['determinant']:.2f}")
m3.metric("Indice de Armonia", f"{analysis['harmony_score']} / 10")
m4.metric("Topologia del sistema", analysis['classification'])

st.success(f"**Diagnostico Psicodinamico:** {analysis['psychological_summary']}")

st.markdown("---")

st.subheader("Sensibilidad a las Primeras Impresiones ($t=0$)")
init_analysis = InitialConditionAnalyzer.analyze_initial_vector(r0, j0, a, b, c, d)

i1, i2, i3 = st.columns(3)
i1.metric("Cuadrante Emocional Inicial", init_analysis["initial_quadrant"])
i2.metric("Velocidad de Cambio ($dR/dt, dJ/dt$)", f"({init_analysis['velocity_vector']['dR/dt']:.2f}, {init_analysis['velocity_vector']['dJ/dt']:.2f})")
i3.metric("Magnitud del Impulso", f"{init_analysis['velocity_magnitude']:.2f}")

st.write(f"**Tendencia a Corto Plazo:** {init_analysis['short_term_trend']}")

def simulate_romance(a, b, c ,d, r0, j0, t_max=15.0, n_points=500):
    def system(t, y):
        R, J = y
        dR_dt = a * R + b * J
        dJ_dt = c * R + d * J
        return[dR_dt, dJ_dt]

    t_span = (0, t_max)
    t_eval = np.linspace(0, t_max, n_points)
    sol = solve_ivp(system, t_span, [r0, j0], t_eval=t_eval)
    return sol.t, sol.y[0], sol.y[1]

st.markdown("---")
st.subheader("Visualizacion Dinamica de la Relacion")

t_vals, r_vals, j_vals = simulate_romance(a, b, c, d, r0, j0)

col_plot1, col_plot2 = st.columns(2)

with col_plot1:
    st.markdown("## Evolucion Temporal")
    st.markdown("Como cambian los sentimientos de ambos a lo largo del tiempo.")

    fig_time, ax_time = plt.subplots(figsize=(6, 4))
    ax_time.plot(t_vals, r_vals, label="Romeo (R)", color="#ff4b4b", linewidth=2)
    ax_time.plot(t_vals, j_vals, label="Juileta (J)", color="#7b1fa2", linewidth=2)
    ax_time.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax_time.set_xlabel("Tiempo ($t$)")
    ax_time.set_ylabel("Nivel de sentimiento")
    ax_time.legend()
    ax_time.grid(True, linestyle=":", alpha=0.6)
    st.pyplot(fig_time)

with col_plot2:
    st.markdown("### Espacio de Fase (Trayectoria)")
    st.markdown("Relacion directa entre el amor de Romeo y Julieta.")

    fig_phase, ax_phase = plt.subplots(figsize=(6,4))
    ax_phase.plot(r_vals, j_vals, color="#0083b8", linewidth=2)
    ax_phase.scatter([r0], [j0], color="green", s=50, zorder=5, label="Inicio (R0, J0)")
    ax_phase.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax_phase.axvline(0, color="gray", linestyle="--", alpha=0.5)
    ax_phase.set_xlabel("Amor de Romeo ($R$)")
    ax_phase.set_ylabel("Amor de Julieta ($J$)")
    ax_phase.legend()
    ax_phase.grid(True, linestyle=":", alpha=0.6)
    st.pyplot(fig_phase)



