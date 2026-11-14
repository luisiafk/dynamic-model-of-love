from typing import Dict, Any, Tuple
import numpy as np

class InitialConditionAnalyzer:
    @staticmethod
    def classify_quadrant(r: float, j: float) -> str:
        if r > 0 and j > 0:
            return "Amor mutuo"
        elif r < 0 and j < 0:
            return "Odio mutuo"
        elif r > 0 and j < 0:
            return "Romeo ama / Juliet odia"
        elif r < 0 and j > 0:
            return "Romeo odia / Julieta ama"
        else:
            return "Indiferencia"


    @staticmethod
    def analyze_initial_vector(
        r0: float, j0: float, a: float, b: float, c: float, d: float
    ) -> Dict[str, Any]:
        dr_dt = a * r0 + b * j0
        dj_dt = c * r0 + d * j0

        inital_quadrant = InitialConditionAnalyzer.classify_quadrant(r0, j0)

        velocity_magnitude = float(np.sqrt(dr_dt**2 + dj_dt**2))

        #Tendencia a corto plazo
        if dr_dt * r0 > 0 and dj_dt * j0 > 0:
            trend = "Los sentimientos iniciales crecen rapidamente"
        elif dr_dt * r0 < 0 and dj_dt * j0 < 0:
            trend = "Los sentimientos iniciales empiezan a enfriarse"
        else:
            trend = "Dinamica Mixta, evolucion asimetrica"

        return {
            "initial_state" : {"R0": float(r0), "J0": float(j0)},
            "initial_quadrant": inital_quadrant,
            "velocity_vector": {"dR/dt": float(dr_dt), "dJ/dt": float(dj_dt)},
            "velocity_magnitude" : velocity_magnitude,
            "short_term_trend": trend
        }