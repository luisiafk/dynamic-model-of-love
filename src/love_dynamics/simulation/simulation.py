"""
Task 4: Numerical Simulation — SciPy integration.

Orquestador de simulaciones numéricas para los modelos de amor dinámicos.

Integra:
  * Sistemas lineales (1) y (3) con Euler explícito, comparados contra la
    solución analítica de Task 2.
  * Modelo no lineal (4) con scipy.integrate.solve_ivp, para comparar con
    la Fig. 3 del paper de Sprott (2004).

El contrato con los modelos es que expongan un campo vectorial
``rhs(t, y, **params) -> np.ndarray`` (definido en ``models/base.py``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Tuple

import numpy as np

from love_dynamics.analytical import analytical_solution_linear_2d


@dataclass
class SimulationResult:
    """Contenedor de los resultados de una simulación numérica.

    Attributes
    ----------
    t : np.ndarray, shape (n_points,)
        Instantes de tiempo.
    y : np.ndarray, shape (n_vars, n_points)
        Trayectoria. ``y[i, :]`` es la variable i-ésima.
    success : bool
        Si el solver terminó exitosamente.
    message : str
        Mensaje informativo o de error del solver.
    model_name : str
        Nombre del modelo simulado (ej. "linear_2d", "nonlinear_2d").
    method : str
        Método usado ("Euler", "RK45", etc.).
    params : dict
        Parámetros del modelo usados en la simulación.
    """

    t: np.ndarray
    y: np.ndarray
    success: bool
    message: str
    model_name: str
    method: str
    params: Dict[str, Any] = field(default_factory=dict)


class LoveSimulator:
    """Simulador de sistemas de ODEs de dinámica del amor."""

    # ------------------------------------------------------------------
    # 1. Euler explícito (sistemas lineales (1) y (3))
    # ------------------------------------------------------------------
    @staticmethod
    def euler_integrate(
        rhs: Callable[[float, np.ndarray], np.ndarray],
        y0: np.ndarray | list[float],
        t_span: Tuple[float, float],
        dt: float,
        model_name: str = "euler",
        **params: Any,
    ) -> SimulationResult:
        """Integración explícita de Euler: y_{n+1} = y_n + dt * f(t_n, y_n).

        Parámetros
        ----------
        rhs : callable
            Campo vectorial ``rhs(t, y, **params)`` que devuelve dy/dt.
        y0 : array-like, shape (n_vars,)
            Condiciones iniciales.
        t_span : tuple (t0, tf)
            Intervalo de integración.
        dt : float
            Paso de tiempo fijo.
        model_name : str
            Etiqueta del modelo para el resultado.
        **params : dict
            Parámetros adicionales pasados a ``rhs``.

        Retorna
        -------
        SimulationResult
        """
        t0, tf = float(t_span[0]), float(t_span[1])
        if dt <= 0:
            raise ValueError("dt debe ser positivo.")
        if tf <= t0:
            raise ValueError("t_span[1] debe ser mayor que t_span[0].")

        n_steps = int(np.ceil((tf - t0) / dt)) + 1
        t = np.linspace(t0, tf, n_steps)
        y0_arr = np.asarray(y0, dtype=float).reshape(-1)
        n_vars = y0_arr.size

        y = np.zeros((n_vars, n_steps), dtype=float)
        y[:, 0] = y0_arr

        for i in range(n_steps - 1):
            ti = t[i]
            yi = y[:, i]
            dyi = np.asarray(rhs(ti, yi, **params), dtype=float).reshape(-1)
            if dyi.size != n_vars:
                raise ValueError(
                    f"rhs devolvió {dyi.size} componentes, se esperaban {n_vars}."
                )
            y[:, i + 1] = yi + dt * dyi

        return SimulationResult(
            t=t,
            y=y,
            success=True,
            message="Integración de Euler completada.",
            model_name=model_name,
            method="Euler",
            params=params,
        )

    # ------------------------------------------------------------------
    # 2. Comparación Euler vs Analítico (Task 2)
    # ------------------------------------------------------------------
    @staticmethod
    def compare_euler_vs_analytical(
        a: float,
        b: float,
        c: float,
        d: float,
        y0: np.ndarray | list[float],
        t_span: Tuple[float, float],
        dt: float,
        analytical_fn: Callable[..., np.ndarray] = analytical_solution_linear_2d,
    ) -> Dict[str, Any]:
        """Compara integración de Euler contra la solución analítica de Task 2.

        Resuelve el sistema lineal 2D:

            dR/dt = a*R + b*J
            dJ/dt = c*R + d*J

        con Euler explícito y con la solución exacta de Task 2, calculando
        el error absoluto en cada paso.

        Parámetros
        ----------
        a, b, c, d : float
            Parámetros románticos (matriz A).
        y0 : array-like, shape (2,)
            Condiciones iniciales [R(0), J(0)].
        t_span : tuple (t0, tf)
            Intervalo de integración.
        dt : float
            Paso de tiempo para Euler.
        analytical_fn : callable, opcional
            Función que devuelve la solución analítica con la firma
            ``analytical_fn(a, b, c, d, y0, t_eval) -> np.ndarray``.
            Por defecto usa ``analytical_solution_linear_2d`` de Task 2.

        Retorna
        -------
        dict con claves:
            t : np.ndarray
            y_euler : np.ndarray, shape (2, n)
            y_analytical : np.ndarray, shape (2, n)
            error_abs : np.ndarray, shape (2, n)  (|y_euler - y_analytical|)
            error_max_R : float
            error_max_J : float
            error_mean_R : float
            error_mean_J : float
        """
        # 1) Solución analítica (Task 2)
        t0, tf = float(t_span[0]), float(t_span[1])
        n_steps = int(np.ceil((tf - t0) / dt)) + 1
        t_eval = np.linspace(t0, tf, n_steps)

        y_analytical = analytical_fn(a, b, c, d, y0, t_eval)
        if y_analytical.shape != (2, n_steps):
            raise ValueError(
                f"La función analítica devolvió shape {y_analytical.shape}, "
                f"se esperaba (2, {n_steps})."
            )

        # 2) Euler explícito usando el RHS lineal
        def rhs_linear(t: float, y: np.ndarray, **kwargs: Any) -> np.ndarray:
            R, J = y
            return np.array([a * R + b * J, c * R + d * J], dtype=float)

        euler_result = LoveSimulator.euler_integrate(
            rhs=rhs_linear,
            y0=y0,
            t_span=t_span,
            dt=dt,
            model_name="linear_2d",
        )

        y_euler = euler_result.y
        if y_euler.shape != y_analytical.shape:
            raise ValueError(
                f"Euler devolvió shape {y_euler.shape}, "
                f"se esperaba {y_analytical.shape}."
            )

        # 3) Errores
        error_abs = np.abs(y_euler - y_analytical)
        error_max_R = float(np.max(error_abs[0]))
        error_max_J = float(np.max(error_abs[1]))
        error_mean_R = float(np.mean(error_abs[0]))
        error_mean_J = float(np.mean(error_abs[1]))

        return {
            "t": t_eval,
            "y_euler": y_euler,
            "y_analytical": y_analytical,
            "error_abs": error_abs,
            "error_max_R": error_max_R,
            "error_max_J": error_max_J,
            "error_mean_R": error_mean_R,
            "error_mean_J": error_mean_J,
            "euler_result": euler_result,
        }

    # ------------------------------------------------------------------
    # 3. Modelo no lineal (4) con solve_ivp (SciPy)
    # ------------------------------------------------------------------
    @staticmethod
    def simulate_nonlinear(
        rhs: Callable[[float, np.ndarray], np.ndarray],
        y0: np.ndarray | list[float],
        t_span: Tuple[float, float],
        method: str = "RK45",
        t_eval: np.ndarray | None = None,
        model_name: str = "nonlinear_2d",
        **params: Any,
    ) -> SimulationResult:
        """Integración del modelo no lineal con scipy.integrate.solve_ivp.

        Usado para el modelo no lineal (4) con saturación, comparando
        visualmente contra la Fig. 3 del paper de Sprott (2004).

        Parámetros
        ----------
        rhs : callable
            Campo vectorial ``rhs(t, y, **params)``.
        y0 : array-like, shape (n_vars,)
            Condiciones iniciales.
        t_span : tuple (t0, tf)
            Intervalo de integración.
        method : str
            Método de solve_ivp ("RK45", "DOP853", "Radau", etc.).
        t_eval : np.ndarray, opcional
            Instantes donde se quiere la solución. Si None, se generan 1000
            puntos equiespaciados en t_span.
        model_name : str
            Etiqueta del modelo.
        **params : dict
            Parámetros adicionales pasados a ``rhs``.

        Retorna
        -------
        SimulationResult
        """
        try:
            from scipy.integrate import solve_ivp
        except ImportError as exc:
            raise ImportError(
            ) from exc

        t0, tf = float(t_span[0]), float(t_span[1])
        if tf <= t0:
            raise ValueError("t_span[1] debe ser mayor que t_span[0].")

        if t_eval is None:
            t_eval = np.linspace(t0, tf, 1000)

        sol = solve_ivp(
            fun=lambda t, y: np.asarray(rhs(t, y, **params), dtype=float),
            t_span=(t0, tf),
            y0=np.asarray(y0, dtype=float).reshape(-1),
            method=method,
            t_eval=t_eval,
            dense_output=False,
        )

        if not sol.success:
            return SimulationResult(
                t=sol.t,
                y=sol.y,
                success=False,
                message=sol.message or "solve_ivp falló sin mensaje.",
                model_name=model_name,
                method=method,
                params=params,
            )

        return SimulationResult(
            t=sol.t,
            y=sol.y,
            success=True,
            message="Integración no lineal completada con solve_ivp.",
            model_name=model_name,
            method=method,
            params=params,
        )


__all__ = ["LoveSimulator", "SimulationResult"]
