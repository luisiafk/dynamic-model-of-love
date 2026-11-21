"""
Linear 2D love model — Romeo & Julieta (System 1).

dR/dt = a*R + b*J
dJ/dt = c*R + d*J

where (a, b) specify Romeo's romantic style and (c, d) specify Juliet's.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from .base import BaseLoveModel


class LinearLoveModel(BaseLoveModel):
    """Linear two-individual love affair (Romeo & Julieta).

    Parameters
    ----------
    name : str
        Model name.
    a, b, c, d : float
        Romantic style parameters.
    """

    def __init__(
        self,
        name: str = "linear_2d",
        a: float = 1.0,
        b: float = 1.0,
        c: float = 1.0,
        d: float = 1.0,
    ) -> None:
        super().__init__(name=name, params={"a": a, "b": b, "c": c, "d": d})
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def rhs(self, t: float, y: np.ndarray, **params: Any) -> np.ndarray:
        """Compute dy/dt for the linear Romeo & Julieta system.

        Parameters
        ----------
        t : float
            Current time (unused, system is autonomous).
        y : np.ndarray, shape (2,)
            State vector [R, J].
        **params : dict
            Optional override parameters a, b, c, d. Falls back to instance
            attributes when not provided.

        Returns
        -------
        np.ndarray, shape (2,)
            [dR/dt, dJ/dt].
        """
        y = np.asarray(y, dtype=float).reshape(-1)
        if y.size != 2:
            raise ValueError("LinearLoveModel expects a state vector of size 2.")

        a = params.get("a", self.a)
        b = params.get("b", self.b)
        c = params.get("c", self.c)
        d = params.get("d", self.d)

        R, J = y
        return np.array([a * R + b * J, c * R + d * J], dtype=float)


__all__ = ["LinearLoveModel"]
