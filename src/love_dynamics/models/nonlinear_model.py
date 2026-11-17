"""
Non-linear 2D love model with saturation (System 4).

Includes linear romantic-style terms plus nonlinear saturation that bounds
emotions so they do not grow without limit.

dR/dt = a*R + b*J - k_R * R * (R^2 + J^2)
dJ/dt = c*R + d*J - k_J * J * (R^2 + J^2)
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from .base import BaseLoveModel


class NonlinearLoveModel(BaseLoveModel):
    """Non-linear two-individual love model with emotional saturation.

    Parameters
    ----------
    name : str
        Model name.
    a, b, c, d : float
        Romantic style parameters (same meaning as the linear model).
    k_R, k_J : float
        Saturation coefficients for Romeo and Julieta respectively.
    """

    def __init__(
        self,
        name: str = "nonlinear_2d",
        a: float = 1.0,
        b: float = 1.0,
        c: float = 1.0,
        d: float = 1.0,
        k_R: float = 0.1,
        k_J: float = 0.1,
    ) -> None:
        super().__init__(
            name=name,
            params={"a": a, "b": b, "c": c, "d": d, "k_R": k_R, "k_J": k_J},
        )
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.k_R = k_R
        self.k_J = k_J

    def rhs(self, t: float, y: np.ndarray, **params: Any) -> np.ndarray:
        """Compute dy/dt for the non-linear saturated system.

        Parameters
        ----------
        t : float
            Current time (unused, system is autonomous).
        y : np.ndarray, shape (2,)
            State vector [R, J].
        **params : dict
            Optional override parameters a, b, c, d, k_R, k_J.

        Returns
        -------
        np.ndarray, shape (2,)
            [dR/dt, dJ/dt].
        """
        y = np.asarray(y, dtype=float).reshape(-1)
        if y.size != 2:
            raise ValueError("NonlinearLoveModel expects a state vector of size 2.")

        a = params.get("a", self.a)
        b = params.get("b", self.b)
        c = params.get("c", self.c)
        d = params.get("d", self.d)
        k_R = params.get("k_R", self.k_R)
        k_J = params.get("k_J", self.k_J)

        R, J = y
        r2 = R * R + J * J

        dR = a * R + b * J - k_R * R * r2
        dJ = c * R + d * J - k_J * J * r2

        return np.array([dR, dJ], dtype=float)


__all__ = ["NonlinearLoveModel"]
