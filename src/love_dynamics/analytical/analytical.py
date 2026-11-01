"""
Task 2: Analytical Analysis — Eigenvalues & Exact Solutions.

PARCHE MÍNIMO para interoperar con Task 4 (Simulación Numérica).

Esta función es el contrato que Task 4 espera para comparar Euler contra
la solución analítica del sistema lineal 2D (Romeo & Julieta):

    dR/dt = a*R + b*J
    dJ/dt = c*R + d*J

Mientras quien implemente Task 2 escribe la solución analítica real, este
stub devuelve ceros con la forma correcta para que Task 4 no rompa.
"""

from __future__ import annotations

import numpy as np
from typing import Tuple, Union


def analytical_solution_linear_2d(
    a: float,
    b: float,
    c: float,
    d: float,
    y0: Union[Tuple[float, float], np.ndarray],
    t_eval: np.ndarray,
) -> np.ndarray:
    """
    Solución analítica exacta del sistema lineal 2D.

    Parámetros
    ----------
    a, b, c, d : float
        Parámetros románticos (matriz A = [[a, b], [c, d]]).
    y0 : array-like, shape (2,)
        Condiciones iniciales [R(0), J(0)].
    t_eval : np.ndarray, shape (n,)
        Instantes de tiempo donde se evalúa la solución.

    Retorna
    -------
    np.ndarray, shape (2, n)
        Y[0, :] = R(t), Y[1, :] = J(t) en cada instante de t_eval.

    IMPORTANTE para quien implemente Task 2 definitivamente:
    ---------------------------------------------------------
    - Debe devolver exactamente np.ndarray de shape (2, len(t_eval)).
    - Y[0, :] corresponde a R(t), Y[1, :] a J(t).
    - No cambiar la firma de esta función: Task 4 la importa y llama tal cual.
    - Casos especiales del enunciado a soportar:
        * a = d = 0           ("out of touch")
        * c = -b, d = -a      ("fire and ice")
        * c =  b, d =  a      ("peas in a pod")
    """
    # TODO(Task 2): implementar solución analítica real aquí.
    # Por ahora devuelve ceros con la forma correcta para no romper Task 4.
    return np.zeros((2, len(t_eval)), dtype=float)


__all__ = ["analytical_solution_linear_2d"]