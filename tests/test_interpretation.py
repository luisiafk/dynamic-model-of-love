""" Pruebas unitarias para los módulos de la Tarea 5 (Interpretación Psicológica y Dinámica). Valida arquetipos, estabilidad topológica, condiciones iniciales y generación de informes. """
import pytest
import pandas as pd
from pathlib import Path
from love_dynamics.interpretation.romantic_styles import RomanticStyleClassifier, RomanticStyleCategory
from love_dynamics.interpretation.dynamical_interpretation import analyze_dyadic_relationship
from love_dynamics.interpretation.initial_conditions import InitialConditionAnalyzer
from love_dynamics.interpretation.comparison import DyadicComparisonMatrix
from love_dynamics.interpretation.report import ReportGenerator

def test_romantic_style_classifier():
    """Valida la correcta clasificación de los 4 arquetipos de Sprott (2004)."""
    # Eager Beaver: a > 0, b > 0
    profile_eb = RomanticStyleClassifier.classify(1.0, 1.0)
    assert profile_eb.category == RomanticStyleCategory.EAGER_BEAVER
    # Narcissistic Nerd: a > 0, b < 0
    profile_nn = RomanticStyleClassifier.classify(1.0, -1.0)
    assert profile_nn.category == RomanticStyleCategory.NARCISSISTIC

    # Cautious Lover: a < 0, b > 0
    profile_cl = RomanticStyleClassifier.classify(-1.0, 1.0)
    assert profile_cl.category == RomanticStyleCategory.CAUTIOUS

    # Hermit: a < 0, b < 0
    profile_h = RomanticStyleClassifier.classify(-1.0, -1.0)
    assert profile_h.category == RomanticStyleCategory.HERMIT

def test_dynamical_interpretation_saddle():
    """Verifica que un determinante negativo resulte en un punto silla (Saddle Point)."""
    # Matriz con ad - bc < 0 (ej: a=0, b=1, c=1, d=0 -> det = -1)
    analysis = analyze_dyadic_relationship(a=0.0, b=1.0, c=1.0, d=0.0)
    assert analysis["determinant"] < 0.0
    assert "Saddle Point" in analysis["classification"]

def test_dynamical_interpretation_stable():
    """Verifica que traza negativa y determinante positivo generen estabilidad."""
    analysis = analyze_dyadic_relationship(a=-1.0, b=1.0, c=-1.0, d=-1.0)
    assert analysis["trace"] < 0
    assert analysis["determinant"] > 0

def test_initial_conditions_analysis():
    """Comprueba el cálculo del vector de velocidad inicial y cuadrantes."""
    analysis = InitialConditionAnalyzer.analyze_initial_vector( r0=1.0, j0=1.0, a=1.0, b=1.0, c=1.0, d=1.0 )
    assert analysis["initial_quadrant"] == "Amor mutuo"
    assert analysis["velocity_vector"]["dR/dt"] == 2.0
    assert analysis["velocity_vector"]["dJ/dt"] == 2.0

def test_comparison_matrix_dimensions():
    """Asegura que la matriz cruzada genere exactamente las 16 combinaciones (4x4)."""
    df = DyadicComparisonMatrix.generate_matrix()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 16
    assert "Romeo_Style" in df.columns
    assert "Juliet_Style" in df.columns
    assert "Topology" in df.columns

def test_report_generator_outputs(tmp_path):
    """Verifica que los reportes en Markdown y LaTeX se creen de forma exitosa."""
    md_test_path = tmp_path / "task_5_report.md"
    tex_test_path = tmp_path / "task_5_report.tex"
    ReportGenerator.generate_markdown_report(str(md_test_path))
    ReportGenerator.generate_latex_report(str(tex_test_path))

    assert md_test_path.exists()
    assert tex_test_path.exists()
    assert len(md_test_path.read_text(encoding="utf-8")) > 100
    assert len(tex_test_path.read_text(encoding="utf-8")) > 100