"""
Task 4: Numerical Simulation — exports.

Expone la API pública de simulación para el resto del proyecto.
"""

from .simulation import LoveSimulator, SimulationResult

__all__ = ["LoveSimulator", "SimulationResult"]
