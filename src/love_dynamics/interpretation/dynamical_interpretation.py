import numpy as np
from typing import Dict, Any

def analyze_dyadic_relationship(a: float, b: float, c: float, d:float) -> Dict[str, Any]:
    tr = a + d #Traza de la matriz A
    det = a * c - b * d #Determinante de la matriz A
    discriminant = tr**2 - 4 * det # Discriminante del polinomio caracterisitco

    matrix = np.array([[a, b], [c, d]], dtype=float)
    eigenvalues = np.linalg,eigvals(matrix)

    if det < 0:
        classification = "Saddle Point"
        psychological_summary = (
            "Inestabilidad relacional severa. Dependiendo de los sentimientos iniciales "
            "('primeras impresiones'), la pareja diverge inexorablemente hacia el amor mutuo extremo o el odio irrenconciliable."
        )
        harmony_score = 3.0
    elif det > 0:
        if tr < 0:
            if discriminant >= 0:
                classification = "Stable Node"
                psychological_summary = (
                    "Apatia o convergencia hacia el equilibrio cero. Los sentimientos decaen de forma "
                    "monotonica hacia la indiferencia mutua con el tiempo, independientemente de la pasion inicial."
                )
                harmony_score = 4.0
            else:
                classification = "Stable Focus"
                psychological_summary = (
                    "Ciclos de altibajos emocionales (discuciones seguidas de reconciliacion) que se amortiguan "
                    "progresivamente hasta estabilizarse en un estado de tranquilidad neutral."
                )
                harmony_score = 6.0

        elif tr > 0:
            if discriminant >= 0:
                classification = "Unstable Node"
                psychological_summary = (
                    "Escalada emocional descontrolada. Los sentimientos crecen exponencialmente sin limite "
                    "hacia un enamoramiento desmedido o  una hostilidad explosiva masiva."
                )
                harmony_score = 5.0
            else:
                classification = "Unstable Focus"
                psychological_summary = (
                    "Drama romantico en espiral creciente. Las oscilaciones de amor y odio aumentan su amplitud "
                    "de ciclo en ciclo de forma explosiva, volviendose psicologicamente insostenible."
                )
                harmony_score = 2.0
        else:
            classification = "Center"
            psychological_summary = (
                "Oscilaciones periodicas eternas. La pareja experimenta un ciclo constante, sin amortiguamiento, "
                "entre el amor y el desamor, repitiendo la historia indefinidamente sin colapsar ni extinguirse."
            )
            harmony_score = 7.0
    else:
        classification = "Degenerate / Non-isolated equilibrium"
        psychological_summary = "Puntos de equilibrio no aislados; alta sensibilidad a perturbaciones externas y estados de trancision continua."
        harmony_score = 1.0

    return {
        "trace": float(tr),
        "determinant": float(det),
        "discriminant": float(discriminant),
        "eigenvalues" : eigenvalues.tolist(),
        "classification" : classification,
        "psychological_summary" : psychological_summary,
        "harmony_score": harmony_score
    }
