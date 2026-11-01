from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, Any

class RomanticStyleCategory(Enum):
    EAGER_BEAVER = "Eager Beaver"
    NARCISSISTIC = "Narcissistic Nerd"
    CAUTIOUS = "Cautious / Secure Lover"
    HERMIT = "Hermit"
    BOUNDARY = "Boundary"

@dataclass
class RomanticStyleProfile:
    category: RomanticStyleCategory
    self_reaction: float
    peer_reaction: float
    description: str
    psychological_summary: str

class RomanticStyleClassifier:
    @staticmethod
    def classify(self_coef: float, peer_coef: float) -> RomanticStyleProfile:
        eps = 1e-9

        if abs(self_coef) < eps or abs(peer_coef) < eps:
            return RomanticStyleProfile(
                category=RomanticStyleCategory.BOUNDARY,
                self_reaction=self_coef,
                peer_reaction=peer_coef,
                description="Coeficiente en el umbral cero (neutralidad estricta).",
                psychological_summary="Comportamiento neutral o de transicion."
            )

        if self_coef > 0 and peer_coef > 0:
            return RomanticStyleProfile(
                category=RomanticStyleCategory.EAGER_BEAVER,
                self_reaction=self_coef,
                peer_reaction=peer_coef,
                description="Estimulado por sus propios sentimientos y por los de su pareja.",
                psychological_summary="Propenso a la escalada pasional, dependencia mutua o amplificacion rapida del afecto."
            )
        elif self_coef > 0 and peer_coef < 0:
            return RomanticStyleProfile(
                category=RomanticStyleCategory.NARCISSISTIC,
                self_reaction=self_coef,
                peer_reaction=peer_coef,
                description="Alimentado por sus propios impulsos internos pero adverso al afecto ajeno.",
                psychological_summary="Muestra distanciamiento defensivo ante las muestras de amor; dinamicas de evitacion."
            )
        elif self_coef < 0 and peer_coef > 0:
            return RomanticStyleProfile(
                category=RomanticStyleCategory.CAUTIOUS,
                self_reaction=self_coef,
                peer_reaction=peer_coef,
                description="Amortigua sus propios impulsos pero responde positivamente al amor del otro.",
                psychological_summary="Perfil equilibrado y seguro; busca la validacion externa manteniendo la estabilidad emocional."
            )
        else:
            return RomanticStyleProfile(
                category=RomanticStyleCategory.HERMIT,
                self_reaction=self_coef,
                peer_reaction=peer_coef,
                description="Retraido ante sus propios sentimientos y repelido por el afecto de la pareja.",
                psychological_summary="Tiende a la apatia, aislamiento o disolucion de los lazos afectivos hacia el colapso(0,0)."
            )

    @staticmethod
    def get_preset_parameter(category: RomanticStyleCategory) -> Tuple[float, float]:
        presets = {
            RomanticStyleCategory.EAGER_BEAVER: (1.0, 1.0),
            RomanticStyleCategory.NARCISSISTIC: (1.0, -1.0),
            RomanticStyleCategory.CAUTIOUS: (-1.0, 1.0),
            RomanticStyleCategory.HERMIT: (-1.0, -1.0),
        }
        return presets.get(category, (0.0, 0.0))


