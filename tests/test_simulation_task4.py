"""
Tests para Task 4: Numerical Simulation.

Verifican las 3 funciones/clases principales de mi implementación:
1. LoveSimulator.euler_integrate
2. LoveSimulator.compare_euler_vs_analytical
3. LoveSimulator.simulate_nonlinear (con scipy)
"""

import numpy as np
import pytest

from love_dynamics.simulation import LoveSimulator, SimulationResult


def test_euler_integrate_shape_and_values():
    """Verifica que euler_integrate devuelve SimulationResult con forma correcta."""
    def rhs(t, y, **params):
        R, J = y
        a, b, c, d = 1.0, 1.0, 1.0, 1.0
        return np.array([a * R + b * J, c * R + d * J], dtype=float)

    result = LoveSimulator.euler_integrate(
        rhs=rhs,
        y0=[1.0, 0.0],
        t_span=(0.0, 1.0),
        dt=0.1,
        model_name="linear_2d_test",
    )

    assert isinstance(result, SimulationResult)
    assert result.y.shape == (2, 11)
    assert result.t.shape == (11,)
    assert result.y[0, 0] == 1.0
    assert result.y[1, 0] == 0.0
    assert result.success is True
    assert result.method == "Euler"
    assert result.model_name == "linear_2d_test"


def test_compare_euler_vs_analytical_returns_expected_keys():
    """Verifica que compare_euler_vs_analytical devuelve las claves esperadas."""
    comp = LoveSimulator.compare_euler_vs_analytical(
        a=1.0, b=1.0, c=1.0, d=1.0,
        y0=[1.0, 0.0],
        t_span=(0.0, 1.0),
        dt=0.1,
    )

    expected_keys = {
        "t", "y_euler", "y_analytical", "error_abs",
        "error_max_R", "error_max_J", "error_mean_R", "error_mean_J",
        "euler_result",
    }
    assert expected_keys.issubset(comp.keys())
    assert comp["y_euler"].shape == (2, 11)
    assert comp["y_analytical"].shape == (2, 11)
    assert comp["error_abs"].shape == (2, 11)
    assert isinstance(comp["error_max_R"], float)
    assert isinstance(comp["error_mean_R"], float)


def test_compare_euler_vs_analytical_initial_conditions():
    """Verifica condiciones iniciales en Euler y formato del stub analítico."""
    comp = LoveSimulator.compare_euler_vs_analytical(
        a=0.0, b=1.0, c=1.0, d=0.0,
        y0=[1.0, 1.0],
        t_span=(0.0, 0.5),
        dt=0.1,
    )
    # Euler debe respetar y0 en t=0
    assert np.isclose(comp["y_euler"][0, 0], 1.0)
    assert np.isclose(comp["y_euler"][1, 0], 1.0)
    # Analítico stub devuelve ceros con forma correcta (Task 2 lo implementará)
    assert comp["y_analytical"].shape == (2, 6)
    assert comp["error_abs"].shape == (2, 6)


def test_simulate_nonlinear_with_solve_ivp():
    """Verifica simulate_nonlinear con scipy.integrate.solve_ivp."""
    def rhs_nl(t, y, **params):
        R, J = y
        # Modelo lineal simple para test (suficiente para verificar integración)
        return np.array([R + J, R - J], dtype=float)

    res = LoveSimulator.simulate_nonlinear(
        rhs=rhs_nl,
        y0=[1.0, 0.0],
        t_span=(0.0, 2.0),
        method="RK45",
        model_name="test_nonlinear",
    )

    assert isinstance(res, SimulationResult)
    assert res.success is True
    assert res.method == "RK45"
    assert res.model_name == "test_nonlinear"
    assert res.y.shape[0] == 2
    assert res.t.shape[0] > 0
    assert np.isclose(res.y[0, 0], 1.0)
    assert np.isclose(res.y[1, 0], 0.0)


def test_simulate_nonlinear_custom_t_eval():
    """Verifica que t_eval se respeta en simulate_nonlinear."""
    def rhs(t, y, **params):
        return np.array([-y[0], -y[1]], dtype=float)

    t_eval = np.linspace(0, 1, 51)
    res = LoveSimulator.simulate_nonlinear(
        rhs=rhs,
        y0=[1.0, 2.0],
        t_span=(0.0, 1.0),
        t_eval=t_eval,
    )
    assert res.y.shape == (2, len(t_eval))
    assert np.allclose(res.t, t_eval)
