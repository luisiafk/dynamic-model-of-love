"""
Task 4: Generador de gráficas mínimas viables.

Genera:
1) Series temporales R(t), J(t) para sistemas lineales (1) con Euler
3) Gráficas del modelo no lineal (4) con solve_ivp (series temporales + plano fase numérico)

Guarda:
- Figuras en: results/figures/task4/
- Datos (.npz) en: results/simulations/task4/
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Asegurar src/ en path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from love_dynamics.simulation import LoveSimulator
from love_dynamics.simulation.plotting import Task4Plotter


def main():
    base_dir = ROOT
    figs_dir = base_dir / "results" / "figures" / "task4"
    sims_dir = base_dir / "results" / "simulations" / "task4"
    figs_dir.mkdir(parents=True, exist_ok=True)
    sims_dir.mkdir(parents=True, exist_ok=True)

    print("=== Task 4: Generando gráficas mínimas viables ===")
    print(f"Figuras: {figs_dir}")
    print(f"Simulaciones: {sims_dir}")
    print()

    # ============================================================
    # GRÁFICA 1: SERIES TEMPORALES R(t), J(t) - SISTEMA LINEAL (1) CON EULER
    # ============================================================
    print("[1/3] Integrando sistemas lineales (1) con Euler...")

    linear_styles = {
        "Eager Beaver (+,+,+,+)": {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0, "y0": [1.0, 0.0]},
        "Cautious (-,+,-,+)": {"a": -0.5, "b": 1.0, "c": -0.5, "d": 1.0, "y0": [1.0, 0.0]},
        "Hermit (-,-,-,-)": {"a": -1.0, "b": -0.5, "c": -0.5, "d": -1.0, "y0": [1.0, 1.0]},
        "Fire and ice (1,1,-1,-1)": {"a": 1.0, "b": 1.0, "c": -1.0, "d": -1.0, "y0": [1.0, 0.0]},
    }

    linear_results = {}
    for name, cfg in linear_styles.items():
        a, b, c, d = cfg["a"], cfg["b"], cfg["c"], cfg["d"]
        y0 = cfg["y0"]

        def make_rhs(a=a, b=b, c=c, d=d):
            def rhs(t, y, **params):
                R, J = y
                return np.array([a * R + b * J, c * R + d * J], dtype=float)
            return rhs

        res = LoveSimulator.euler_integrate(
            rhs=make_rhs(),
            y0=y0,
            t_span=(0.0, 10.0),
            dt=0.01,
            model_name=f"linear_2d_{name}",
            a=a, b=b, c=c, d=d,
        )
        linear_results[name] = res

        # Guardar datos
        np.savez(
            sims_dir / f"linear_{name.replace(' ', '_').replace('(','').replace(')','').replace('+','pos').replace('-','neg').replace(',','_')}.npz",
            t=res.t,
            y=res.y,
            a=a, b=b, c=c, d=d,
            y0=y0,
        )
        print(f"  -> {name}: OK (shape={res.y.shape})")

    # Guardar figura 1
    fig1 = Task4Plotter.plot_time_series(
        linear_results,
        title="Series temporales R(t), J(t) - Sistema lineal con Euler",
        figsize=(14, 10),
        save_path=str(figs_dir / "01_series_temporales_lineal_euler.png"),
    )
    plt.close(fig1)

    # ============================================================
    # GRÁFICA 3: MODELO NO LINEAL (4) CON solve_ivp
    # ============================================================
    print()
    print("[2/3] Integrando modelo no lineal (4) con solve_ivp...")

    # Intentar reproducir Fig. 3 de Sprott (2004) - parámetros típicos
    nonlinear_cases = {
        "Caso típico Fig.3 (a=-3, b=0, R0=0.01, J0=0)": {"a": -3.0, "b": 0.0, "R0": 0.01, "J0": 0.0, "t_span": (0.0, 50.0)},
        "Con perturbación (a=-3, b=0, R0=0.01, J0=0.01)": {"a": -3.0, "b": 0.0, "R0": 0.01, "J0": 0.01, "t_span": (0.0, 50.0)},
    }

    nonlinear_results = {}
    for name, cfg in nonlinear_cases.items():
        a_nl = cfg["a"]
        b_nl = cfg["b"]
        R0, J0 = cfg["R0"], cfg["J0"]
        t_span_nl = cfg["t_span"]

        def make_rhs_nl(a_nl=a_nl, b_nl=b_nl):
            def rhs_nl(t, y, **params):
                R, J = y
                # Modelo no lineal tipo Sprott (forma simplificada)
                # dR/dt = J
                # dJ/dt = -R + a*J + b*R^2 + J^2
                dR_dt = J
                dJ_dt = -R + a_nl * J + b_nl * R * R + J * J
                return np.array([dR_dt, dJ_dt], dtype=float)
            return rhs_nl

        try:
            res_nl = LoveSimulator.simulate_nonlinear(
                rhs=make_rhs_nl(),
                y0=[R0, J0],
                t_span=t_span_nl,
                method="RK45",
                model_name=f"nonlinear_2d_{name}",
                a=a_nl, b=b_nl,
            )
            nonlinear_results[name] = res_nl

            np.savez(
                sims_dir / f"nonlinear_{name.replace(' ', '_').replace('(','').replace(')','').replace(',','_').replace('=','_')}.npz",
                t=res_nl.t,
                y=res_nl.y,
                a=a_nl, b=b_nl,
                y0=[R0, J0],
            )
            print(f"  -> {name}: OK (shape={res_nl.y.shape}, success={res_nl.success})")
        except Exception as e:
            print(f"  -> {name}: ERROR - {e}")

    if nonlinear_results:
        # Series temporales no lineal
        fig3_ts = Task4Plotter.plot_time_series_nonlinear(
            nonlinear_results,
            title="Series temporales modelo no lineal con solve_ivp",
            figsize=(14, 6),
            save_path=str(figs_dir / "03a_series_temporales_nolineal_solveivp.png"),
        )
        plt.close(fig3_ts)

        # Plano fase numérico no lineal
        fig3_ph = Task4Plotter.plot_phase_plane_nonlinear(
            nonlinear_results,
            title="Plano fase numérico R vs J - Modelo no lineal con solve_ivp",
            figsize=(10, 8),
            save_path=str(figs_dir / "03b_plano_fase_numerico_nolineal_solveivp.png"),
        )
        plt.close(fig3_ph)
    else:
        print("  [AVISO] No se generaron resultados no lineales.")

    print()
    print("=== Completado ===")
    print(f"Revisa las gráficas en: {figs_dir}")
    print(f"Datos guardados en: {sims_dir}")
    print()
    print("Gráficas generadas:")
    print("  - task4_01_series_temporales_lineal_euler.png (Gráfica 1)")
    print("  - task4_03a_series_temporales_nolineal_solveivp.png (Gráfica 3a)")
    print("  - task4_03b_plano_fase_numerico_nolineal_solveivp.png (Gráfica 3b)")


if __name__ == "__main__":
    main()
