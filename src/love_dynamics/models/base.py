"""
Base model for love dynamical systems.

Defines the abstract contract that every love model must satisfy so that
Task 4 (Simulation) can integrate them without knowing their internals.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

import numpy as np


class BaseLoveModel(ABC):
    """Abstract base class for dynamical models of love.

    Every concrete model must implement :meth:`rhs` so that the simulator
    in ``task_4_simulation`` can integrate it generically.
    """

    def __init__(self, name: str, params: Dict[str, float] | None = None) -> None:
        """Initialize the model.

        Parameters
        ----------
        name : str
            Human-readable name of the model.
        params : dict, optional
            Dictionary of model parameters. Stored for reference and passed
            to :meth:`rhs` when not overridden at call time.
        """
        self.name = name
        self.params: Dict[str, float] = dict(params or {})

    @abstractmethod
    def rhs(self, t: float, y: np.ndarray, **params: Any) -> np.ndarray:
        """Right-hand side of the ODE system: dy/dt = f(t, y, **params).

        Parameters
        ----------
        t : float
            Current time.
        y : np.ndarray, shape (n_vars,)
            Current state vector.
        **params : dict
            Additional model-specific parameters. If empty, the values
            stored in ``self.params`` are used.

        Returns
        -------
        np.ndarray, shape (n_vars,)
            Time derivative of the state vector.
        """
        ...

    def __call__(self, t: float, y: np.ndarray, **params: Any) -> np.ndarray:
        """Allow calling the model as a function: model(t, y)."""
        return self.rhs(t, y, **params)

    def get_params(self) -> Dict[str, float]:
        """Return a copy of the stored parameters."""
        return dict(self.params)

    def set_params(self, params: Dict[str, float]) -> None:
        """Replace the stored parameters."""
        self.params = dict(params)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, params={self.params!r})"


__all__ = ["BaseLoveModel"]
