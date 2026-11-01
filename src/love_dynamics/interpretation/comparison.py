import pandas as pd
from typing import List, Dict, Any
from .romantic_styles import RomanticStyleCategory
from .dynamical_interpretation import analyze_dyadic_relationship

class DyadicComparisonMatrix:
    @staticmethod
    def generate_matrix() -> pd.DataFrame:
        archetypes = {
            "Eager Beaver": (1.0, 1.0),
            "Narcissist": (1.0, -1.0),
            "Cautious Lover": (-1.0, 1.0),
            "Hermit": (-1.0, -1.0)
        }

        records: List[Dict[str, Any]] = []

        for r_name, (a, b) in archetypes.items():
            for j_name, (d, c) in archetypes.items():
                analysis = analyze_dyadic_relationship(a=a, b=b, c=c, d=d)

                records.append({
                    "Romeo_Style": r_name,
                    "Juliet_Style": j_name,
                    "Trace": analysis["trace"],
                    "Determinant": analysis["determinant"],
                    "Topology": analysis["classification"],
                    "Harmony_Score": analysis["harmony_score"],
                    "Summary": analysis["psychological_summary"]
                })
        return pd.DataFrame(records)